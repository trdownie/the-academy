from django.shortcuts import render
from .models import Subject

# Create your views here.

def display_index(request):
    return render(request, '')