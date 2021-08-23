from django.shortcuts import render
from .models import Subject, Article

# Create your views here.

def all_articles(request):
    """ view to show all articles, including sorting/searching """

    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'articles/articles.html', context)