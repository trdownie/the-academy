from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Subject, Article
from .forms import ArticleForm


def all_articles(request):
    """View to show all articles, including filtering/sorting/searching"""

    # Get all articles
    articles = Article.objects.all()
    # Set filtering/sorting/searching criteria to none
    query = None
    subjects = None
    sort = None
    direction = None
    proposals = False

    # On a get request
    if request.GET:

        # If 'proposals' exists (via the proposals toggle)
        # then filter articles accordingly
        if 'proposals' in request.GET:
            articles = Article.objects.filter(proposal=True)
            proposals = True
            messages.info(request, f'Showing proposals only')

        # If a sort parameter is defined
        if 'sort' in request.GET:
            # Define sortkey as this parameter
            sortkey = request.GET['sort']
            sort = sortkey  # (to preserve sort)

            # If sorting by article title, add a temporary lowercase field
            # to the article model & update the sortkey accordingly
            if sortkey == 'title':
                sortkey = 'lowercase_title'
                articles = articles.annotate(lowercase_title=Lower('title'))

            # Determine whether a direction parameter is defined
            if 'direction' in request.GET:
                # Define direction as this parameter
                direction = request.GET['direction']
                # If direction is descending, sort by negative sortkey
                # (since default is ascending and negative will reverse)
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            # If direction is descending, reverse sortkey
            articles = articles.order_by(sortkey)
            messages.info(request, f'Articles sorted by {sort} \
                          in {direction}ending order')

        # Determine whether a subject parameter is defined
        if 'subject' in request.GET:
            # If so, split this parameter into list
            subjects = request.GET['subject'].split(',')
            # Find *distinct* articles with subject names in the list
            articles = articles.filter(
                subjects__subject_name__in=subjects).distinct()
            # Define a list of 'in use' subject names for later use
            subjects = Subject.objects.filter(subject_name__in=subjects)

        # Determine whether a search parameter is defined
        if 'q' in request.GET:
            # If so, obtain this
            query = request.GET['q']
            # If nothing entered, display error message
            if not query:
                messages.error(request, "No search criteria entered!")
                return redirect(reverse('articles'))

            # Obtain articles containing query
            queries = Q(title__icontains=query) | Q(summary__icontains=query)
            articles = articles.filter(queries)
            messages.info(request, f'Showing articles containing: {query}')

    template = 'articles/articles.html'
    context = {
        'articles': articles,
        'search_term': query,
        'current_subjects': subjects,
        'proposals': proposals,
    }

    return render(request, template, context)


def article_detail(request, article_id):
    """Show individual article details """
    
    # Obtain article object & return to template
    article = get_object_or_404(Article, pk=article_id)

    template = 'articles/article_detail.html'
    context = {
        'article': article,
    }

    return render(request, template, context)


@login_required
def add_article(request):
    """Add new article to store"""

    # Upon the form submitting (POST)
    if request.method == 'POST':
        # Obtain the form details using the ArticleForm() form
        form = ArticleForm(request.POST, request.FILES)
        # If the form is valid, save it and return to the article detail page
        if form.is_valid():
            article = form.save()
            messages.success(request, 'Article uploaded!')
            return redirect(reverse('article_detail', args=[article.id]))
        # Otherwise, return an error message
        else:
            messages.error(request, 'Article failed to upload. \
                           Please check form!')

    # Upon usual (non-POST) function request, define form using ArticleForm()
    else:
        form = ArticleForm()

    template = 'articles/add_article.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_article(request, article_id):
    """Edit article"""

    # Get the article object in question
    article = get_object_or_404(Article, pk=article_id)

    # If the user is not one of the article's authors
    if not article.authors.filter(user=request.user).exists():
        # And if the user is not a superuser
        if not request.user.is_superuser:
            # Redirect the user to the homepage with a message
            messages.error(request, 'Area for article authors or \
                           senior academics only!')
            return redirect(reverse('home'))

    # Provided user is the author/superuser, upon submitting edit article form
    if request.method == 'POST':
        # Set form as the submitted form
        form = ArticleForm(request.POST, request.FILES, instance=article)
        # Check if the form is valid and if so save it
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated!')
            return redirect(reverse('article_detail', args=[article.id]))
        # Otherwise return an error message
        else:
            messages.error(request, 'Article failed to update. \
                           Please check form!')

    # On other request, use the ArticleForm() form for the article in question
    # and provide a custom message
    else:
        form = ArticleForm(instance=article)
        messages.info(request, f'You are now editing {article.title}')

    template = 'articles/edit_article.html'
    context = {
        'form': form,
        'article': article,
    }

    return render(request, template, context)


@login_required
def delete_article(request, article_id):
    """Delete article"""

    # Get the article object in question
    article = get_object_or_404(Article, pk=article_id)

    # If the user is not one of the article's authors
    if not article.authors.filter(user=request.user).exists():
        # And if the user is not a superuser
        if not request.user.is_superuser:
            messages.error(request, 'Area for authors/senior academics only!')
            return redirect(reverse('home'))

    # Otherwise, delete article with message to confirm
    article.delete()
    messages.success(request, 'Article deleted!')

    return redirect(reverse('articles'))
