from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There are no articles in your bag!")
        return redirect(reverse('articles'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JUwwKI6dywDr6yKBHUYgU7RmbufrYpnBW8j0IRAazOW5oo6kS54uMa5ZNEfeFQVu8aWEllmEOYlJd4UuOTjXebx00oauOUumX',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
