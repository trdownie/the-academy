from django.shortcuts import render, redirect

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

    bag[article_id] = 1

    request.session['bag'] = bag
    
    print(request.session['bag'])
    return redirect(redirect_url)