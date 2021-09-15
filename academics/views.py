from time import sleep

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Academic
from .forms import AcademicProfileForm
from checkout.models import Order
from articles.models import Article


def academic_profile(request, academic_id):
    """
    Show academic profile of other academics
    or user's own profile
    """

    academic = get_object_or_404(Academic, pk=academic_id)

    # When user submits form to update profile, obtain the form,
    # check it is valid, save it, and display a message
    if request.method == 'POST':
        form = AcademicProfileForm(request.POST, request.FILES,
                                   instance=academic)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated, {academic.name}')
        else:
            messages.error(request, 'Profile not updated. Please check form!')

    # Otherwise (i.e., on normal page load) define the form using existing info
    else:
        form = AcademicProfileForm(instance=academic)

    followers = academic.academic_set.all()  # List of followers
    follower_count = followers.count()  # Number of followers
    orders = academic.orders.all()  # List of orders
    articles = academic.article_set.all()  # List of articles submitted

    template = 'academics/academic_profile.html'
    context = {
        'academic': academic,
        'form': form,
        'followers': followers,
        'follower_count': follower_count,
        'articles': articles,
        'orders': orders,
        'on_profile': True,  # To avoid showing shopping bag in success toast
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Show user's order history for any given order
    """

    order = get_object_or_404(Order, order_number=order_number)
    academic = Academic.objects.get(user=request.user)
    messages.info(request, f'This is a confirmation of order {order_number}. \
                  A confirmation email was sent on {order.date}')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,  # To tailor return button
        'academic': academic,
    }

    return render(request, template, context)


def article_detail_profile(request, article_id):
    """Show individual article details (from profile)"""

    article = get_object_or_404(Article, pk=article_id)
    template = 'articles/article_detail.html'
    context = {
        'article': article,
        'from_profile': True,  # To tailor return button
    }

    return render(request, template, context)


def academic_profile_from_profile(request, academic_id):
    """Show academic profile (from own profile)"""

    academic = get_object_or_404(Academic, pk=academic_id)
    followers = academic.academic_set.all()  # List of followers
    follower_count = followers.count()  # Number of followers

    template = 'academics/academic_profile.html'
    context = {
        'academic': academic,
        'followers': followers,
        'follower_count': follower_count,
        'from_profile': True  # To tailor return button
    }

    return render(request, template, context)


def follow(request, academic_id):
    """Follow another academic"""

    academic = Academic.objects.get(user=request.user)
    # Get profile to follow
    to_follow = get_object_or_404(Academic, pk=academic_id)

    # Follow academic whose profile user is on
    # If on own profile, display message (shouldn't happen)
    if academic_id == academic.id:
        messages.error(request, "You can't follow yourself!")

    else:
        # If user is already following them, display message
        if academic.following.filter(id=to_follow.id).exists():
            messages.error(request, f"You're already following {to_follow}!")
        # Otherwise, add them to following list
        else:
            academic.following.add(to_follow)
            academic.save()

    current_profile = Academic.objects.get(pk=academic_id)
    followers = current_profile.academic_set.all()  # List of followers
    follower_count = followers.count()  # Number of followers

    template = 'academics/academic_profile.html'
    context = {
        'academic': current_profile,
        'followers': followers,
        'follower_count': follower_count,
        'on_profile': True,  # To avoid showing shopping bag in success toast
        'following': True,  # To display correct follow/unfollow button
    }

    return render(request, template, context)


def unfollow(request, academic_id):
    """Follow another academic"""

    academic = Academic.objects.get(user=request.user)
    # Get profile to unfollow
    to_unfollow = get_object_or_404(Academic, pk=academic_id)

    # If profile to unfollow is in following list, remove it
    # and save updated academic object, displaying message
    if academic.following.filter(id=to_unfollow.id).exists():
        academic.following.remove(to_unfollow)
        academic.save()
        messages.error(request, f"You're no longer following {to_unfollow}.")
    # Otherwise, display error
    else:
        messages.error(request, f"You're not following {to_unfollow}!")

    current_profile = Academic.objects.get(pk=academic_id)
    followers = current_profile.academic_set.all()  # List of followers
    follower_count = followers.count()  # Number of followers

    template = 'academics/academic_profile.html'
    context = {
        'academic': current_profile,
        'followers': followers,
        'follower_count': follower_count,
        'on_profile': True,  # To avoid showing shopping bag in success toast
        'following': False,  # To display correct follow/unfollow button
    }

    return render(request, template, context)


def unfollow_from_hub(request, academic_id):
    """Unfollow another academic from own profile (HUB)"""

    academic = Academic.objects.get(user=request.user)
    # Get profile to unfollow
    to_unfollow = get_object_or_404(Academic, pk=academic_id)

    # If profile to unfollow is in following list, remove it
    # and save updated academic object, displaying message
    if academic.following.filter(id=to_unfollow.id).exists():
        academic.following.remove(to_unfollow)
        academic.save()
        messages.error(request, f"You're no longer following {to_unfollow}.")
    # Otherwise, display error
    else:
        messages.error(request, f"You're not following {to_unfollow}!")

    followers = academic.academic_set.all()  # List of followers
    follower_count = followers.count()  # Number of followers
    form = AcademicProfileForm(instance=academic)
    orders = academic.orders.all()
    articles = academic.article_set.all()

    template = 'academics/academic_profile.html'
    context = {
        'academic': academic,
        'followers': followers,
        'follower_count': follower_count,
        'form': form,
        'orders': orders,
        'articles': articles,
        'on_profile': True,  # To avoid showing shopping bag in success toast
    }

    return render(request, template, context)
