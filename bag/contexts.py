from django.shortcuts import get_object_or_404
from articles.models import Article


def bag_contents(request):
    """Context making bag data available sitewide"""

    # Set all variables
    bag_articles = []
    bag_total = 0
    article_count = 0
    # Obtain bag from session storage or set it
    bag = request.session.get('bag', {})

    # For each article in bag, add price to bag_total and
    # add items into bag_articles
    for article_id, article_count in bag.items():
        article = get_object_or_404(Article, pk=article_id)
        bag_total += article.price
        bag_articles.append({
            'article_id': article_id,
            'article': article,
        })

    context = {
        'bag_articles': bag_articles,
        'bag_total': bag_total,
        'article_count': article_count,
    }

    return context
