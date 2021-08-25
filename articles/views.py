from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Subject, Article

# Create your views here.

def all_articles(request):
    """ view to show all articles, including sorting/searching """

    articles = Article.objects.all()
    query = None
    subject = None

    if request.GET:
        # determine whether a subject parameter is defined within request
        if 'subject' in request.GET:
            # if so, split this parameter into list
            subjects = request.GET['subject'].split(',')
            # find *distinct* articles with subject names in the list
            articles = articles.filter(subjects__subject_name__in=subjects).distinct()
            # define a list of 'in use' subject names for later use
            subjects = Subject.objects.filter(subject_name__in=subjects)


        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No search criteria entered!")
                return redirect(reverse('articles'))
            
            queries = Q(title__icontains=query) | Q(summary__icontains=query)
            articles = articles.filter(queries)

    context = {
        'articles': articles,
        'search_term': query,
        'current_subjects': subjects,
    }

    return render(request, 'articles/articles.html', context)


def article_detail(request, article_id):
    """ view to show individual article details """

    article = get_object_or_404(Article, pk=article_id)

    context = {
        'article': article,
    }

    return render(request, 'articles/article_detail.html', context)