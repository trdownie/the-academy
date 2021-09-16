import stripe
import json

from django.shortcuts import render, redirect, reverse,
                             get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order
from articles.models import Article
from academics.models import Academic
from academics.forms import AcademicProfileForm
from bag.contexts import bag_contents


@require_POST
def cache_checkout_data(request):
    """
    Add the bag and customer details into the metadata
    of the Stripe payment intent
    """

    # Try to add the metadata and return 200 if successful
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)

    # Return an error message and a 400 if unable to do so
    except Exception as e:
        messages.error(request, 'Error. Payment request not processed \
            please try again.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Render the checkout template
    """

    # Get API connection details
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # When checkout form is submitted, create order
    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)

        # If the order form is valid, get the original bag and
        # add the items to the newly created order item before saving
        if order_form.is_valid():
            order = order_form.save(commit=False)
            bag_total = 0
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for article_id, article_count in bag.items():
                article = get_object_or_404(Article, pk=article_id)
                bag_total += article.price
                order.order_items.add(article)
                order.order_total = bag_total
            order.save()

            # Save the customer info in the session storage for later
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                            args=[order.order_number]))

        # If the order form is not valid, display error
        else:
            messages.error(request, 'There was an error with your form. \
                            Please check your information.')

    # If view called normally (non-POST) display template
    else:
        bag = request.session.get('bag', {})
        # If the bag is empty return to articles with error message
        if not bag:
            messages.error(request, "There are no articles in your bag!")
            return redirect(reverse('articles'))

        # Create payment intent
        current_bag = bag_contents(request)
        current_total = current_bag['bag_total']
        stripe_total = round(current_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # If user is logged in, populate checkout form
        if request.user.is_authenticated:
            try:
                academic = Academic.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': academic.user.get_full_name(),
                    'email': academic.user.email,
                    'phone_number': academic.default_phone_number,
                    'street_address1': academic.default_street_address1,
                    'street_address2': academic.default_street_address2,
                    'town_or_city': academic.default_town_or_city,
                    'county': academic.default_county,
                    'postcode': academic.default_postcode,
                    'country': academic.default_country,
                })
            # If logged in but no academic (somehow), display empty form
            except Academic.DoesNotExist:
                order_form = OrderForm()
        # If user not logged in, display empty form
        else:
            order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Display checkout success page, 
    update profile with 'safe info' details,
    and attach user to order
    """

    # Get the save info details and the new order
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # If user is logged in, attach user to order & save their info
    if request.user.is_authenticated:
        academic = Academic.objects.get(user=request.user)
        order.academic = academic
        order.save()

        # Only save info if box was ticked
        if save_info:
            profile_data = {
                'default_email': order.email,
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_country': order.country,
                'name': order.academic.name,
                'username': order.academic.username,
                'about': order.academic.about,
                'level': order.academic.level,
                'image': order.academic.image,
                'following': order.academic.following,
            }
            academic_profile_form = AcademicProfileForm(profile_data, instance=academic)
            if academic_profile_form.is_valid():
                academic_profile_form.save()

        messages.success(request, f'Order successfully processed. \
            Your order number is {order_number}. A confirmation email \
            will be sent to {order.email}.')

    # Delete bag from session storage
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'academic': academic,
    }

    return render(request, template, context)
