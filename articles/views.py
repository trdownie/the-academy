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
        if 'subject' in request.GET:
            subject = request.GET['subject']
            test_one = subject
            fixed_category = 'history'
            # articles = articles.filter(subject__subject_name__in='The')
            # article_list = articles.filter(subjects__value__in=subjects)
            articles = Article.objects.filter(subjects__subject_name__contains=subject)


            test_two = 'test'
            test_three = 'test'
            test_four = fixed_category

            # subjects = 'history'

            # 

            # subjects = Subject.objects.filter(subject__in=subjects)


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
        # 'current_subjects': subjects,
        'test_one': test_one,
        'test_two': test_two,
        'test_three': test_three,
        'test_four': test_four,
    }

    return render(request, 'articles/articles.html', context)


def article_detail(request, article_id):
    """ view to show individual article details """

    article = get_object_or_404(Article, pk=article_id)

    context = {
        'article': article,
    }

    return render(request, 'articles/article_detail.html', context)