from django.shortcuts import render, get_object_or_404
from .models import Subject, Article

# Create your views here.

def all_articles(request):
    """ view to show all articles, including sorting/searching """

    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'articles/articles.html', context)


def article_detail(request, article_id):
    """ view to show individual article details """

    article = get_object_or_404(Article, pk=article_id)

    context = {
        'article': article,
    }

    return render(request, 'articles/article_detail.html', context)