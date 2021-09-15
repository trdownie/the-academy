from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from articles.models import Article
# Create your views here.


def shopping_bag(request):
    """Render shopping bag contents"""

    template = 'bag/bag.html'
    context = {

    }

    return render(request, template, context)


def add_to_bag(request, article_id):
    """Add article to shopping bag"""

    # Obtain the redirect URL & article info, and get/set the bag
    redirect_url = request.POST.get('redirect_url')
    article = get_object_or_404(Article, pk=article_id)
    bag = request.session.get('bag', {})

    # If the article is already in the bag, send error message
    if article_id in bag:
        messages.error(request, f'Already in bag - {article.title}')
    # Otherwise set the quantity of the items in the bag to 1
    else:
        bag[article_id] = 1
        messages.success(request, f'Added to bag - {article.title}')

    # Overwrite the bag with the new bag
    request.session['bag'] = bag

    return redirect(redirect_url)


def quick_add_to_bag(request, article_id):
    """Add article to shopping bag from index"""

    # Obtain required variables
    articles = Article.objects.all()
    article = get_object_or_404(Article, pk=article_id)
    bag = request.session.get('bag', {})

    # Set item in bag (as above)
    if article_id in bag:
        messages.error(request, f'Already in bag - {article.title}')
    else:
        bag[article_id] = 1
        messages.success(request, f'Added to bag - {article.title}')

    # Overwrite bag
    request.session['bag'] = bag

    template = 'articles/articles.html'
    context = {
        'articles': articles
    }

    return render(request, template, context)


def remove_from_bag(request, article_id):
    """Remove article from shopping bag"""

    # Obtain required variables
    redirect_url = request.POST.get('redirect_url')
    article = get_object_or_404(Article, pk=article_id)
    bag = request.session.get('bag', {})

    # Remove item from bag with message
    bag.pop(article_id)
    messages.warning(request, f'Removed from bag - {article.title}')

    # Overwrite bag
    request.session['bag'] = bag

    return redirect(redirect_url)