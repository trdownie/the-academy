from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from articles.models import Article
# Create your views here.


def shopping_bag(request):
    """ view to render shopping bag contents """

    context = {

    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, article_id):
    """ Add specified article to shopping bag """

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    article = get_object_or_404(Article, pk=article_id)

    if article_id in bag:
        messages.error(request, f'Already in bag - {article.title}')
    else:
        bag[article_id] = 1
        messages.success(request, f'Added to bag - {article.title}')
    
    request.session['bag'] = bag
    return redirect(redirect_url)


def quick_add_to_bag(request, article_id):
    """ Add specified article to shopping bag """

    articles = Article.objects.all()
    bag = request.session.get('bag', {})
    article = get_object_or_404(Article, pk=article_id)

    if article_id in bag:
        messages.error(request, f'Already in bag - {article.title}')
    else:
        bag[article_id] = 1
        messages.success(request, f'Added to bag - {article.title}')
    
    request.session['bag'] = bag
    context = {
        'articles': articles
    }

    return render(request, 'articles/articles.html', context)


def remove_from_bag(request, article_id):
    """ Remove specified article from shopping bag """

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    article = get_object_or_404(Article, pk=article_id)

    bag.pop(article_id)
    messages.warning(request, f'Removed from bag - {article.title}')

    request.session['bag'] = bag
    return redirect(redirect_url)