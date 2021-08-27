from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from articles.models import Article

def bag_contents(request):

    bag_articles = []
    bag_subscriptions = []
    bag_total = 0
    article_count = 0
    subscription_count = 0
    bag = request.session.get('bag', {})

    for article_id, article_count in bag.items():
        article = get_object_or_404(Article, pk=article_id)
        bag_total += article.price
        bag_articles.append({
            'article_id': article_id,
            'article': article,
        })

    context = {
        'bag_articles': bag_articles,
        'bag_subscriptions': bag_subscriptions,
        'bag_total': bag_total,
        'article_count': article_count,
        'subscription_count': subscription_count,
    }

    return context
