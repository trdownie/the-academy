from django.shortcuts import render
from django.contrib import messages

# Create your views here.


def index(request):
    """ view to return index page """
    messages.warning(request, 'WARNING')
    return render(request, 'home/index.html')
