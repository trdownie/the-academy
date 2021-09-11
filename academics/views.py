from time import sleep

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Academic
from .forms import AcademicProfileForm
from checkout.models import Order
from articles.models import Article


def academic_profile(request, academic_id):
    """ view to show individual article details """
    academic = get_object_or_404(Academic, pk=academic_id)

    if request.method == 'POST':
        form = AcademicProfileForm(request.POST, instance=academic)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated, {academic.name}')
        else:
            messages.error(request, 'Profile not updated. Please check form!')
    else:
        form = AcademicProfileForm(instance=academic)
    # academics = Academic.objects.all()
    followers = academic.academic_set.all()
    follower_count = followers.count()
    form = AcademicProfileForm(instance=academic)
    orders = academic.orders.all()
    articles = academic.article_set.all()

    context = {
        'academic': academic,
        'followers': followers,
        'follower_count': follower_count,
        'form': form,
        'orders': orders,
        'on_profile': True,
        'articles': articles
    }

    return render(request, 'academics/academic_profile.html', context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    academic = Academic.objects.get(user=request.user)

    messages.info(request, f'This is a confirmation of order {order_number}. \
                  A confirmation email was sent on {order.date}')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
        'academic': academic,
    }

    return render(request, template, context)


def article_detail_profile(request, article_id):
    """ view to show individual article details """

    article = get_object_or_404(Article, pk=article_id)

    context = {
        'article': article,
        'from_profile': True,
    }

    return render(request, 'articles/article_detail.html', context)


def follow(request, academic_id):
    """ follow another academic """
    academic = Academic.objects.get(user=request.user)
    print(academic_id)
    current_profile = Academic.objects.get(pk=academic_id)
    print(current_profile)

    # follow academic whose profile user is on - WORKING
    if academic_id == academic.id:
        messages.error(request, "You can't follow yourself!")
    else:
        to_follow = get_object_or_404(Academic, pk=academic_id)
        if academic.following.filter(id=to_follow.id).exists():
            messages.error(request, f"You're already following {to_follow}!")
        else:
            academic.following.add(to_follow)
            academic.save()

    followers = academic.academic_set.all()
    follower_count = followers.count()
    form = AcademicProfileForm(instance=academic)
    orders = academic.orders.all()
    articles = academic.article_set.all()

    context = {
        'academic': current_profile,
        'followers': followers,
        'follower_count': follower_count,
        'form': form,
        'orders': orders,
        'on_profile': True,
        'articles': articles,
        'following': True,
    }

    return render(request, 'academics/academic_profile.html', context)


def unfollow(request, academic_id):
    """ follow another academic """
    academic = Academic.objects.get(user=request.user)
    print(academic_id)
    current_profile = Academic.objects.get(pk=academic_id)
    print(current_profile)

    to_unfollow = get_object_or_404(Academic, pk=academic_id)
    if academic.following.filter(id=to_unfollow.id).exists():
        academic.following.remove(to_unfollow)
        academic.save()
        messages.error(request, f"You're no longer following {to_unfollow}.")
    else:
        messages.error(request, f"You're not following {to_unfollow}!")

    followers = academic.academic_set.all()
    follower_count = followers.count() - 1
    form = AcademicProfileForm(instance=academic)
    orders = academic.orders.all()
    articles = academic.article_set.all()

    context = {
        'academic': current_profile,
        'followers': followers,
        'follower_count': follower_count,
        'form': form,
        'orders': orders,
        'on_profile': True,
        'articles': articles,
        'following': False,
    }

    return render(request, 'academics/academic_profile.html', context)