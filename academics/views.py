from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .models import Academic

# Create your views here.


def academic_profile(request, academic_id):
    """ view to show individual article details """

    academic = get_object_or_404(Academic, pk=academic_id)

    context = {
        'academic': academic,
    }

    return render(request, 'academics/academic_profile.html', context)
