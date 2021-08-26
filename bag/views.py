from django.shortcuts import render

# Create your views here.


def shopping_bag(request):
    """ view to render shopping bag contents """



    context = {

    }

    return render(request, 'bag/bag.html', context)