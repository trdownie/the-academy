

def bag_contents(request):

    articles_in_bag = []
    subscriptions_in_bag = []
    bag_total = 5
    article_count = 0
    subscription_count = 0

    context = {
        'articles_in_bag': articles_in_bag,
        'subscriptions_in_bag': subscriptions_in_bag,
        'bag_total': bag_total,
        'article_count': article_count,
        'subscription_count': subscription_count,
    }

    return context
