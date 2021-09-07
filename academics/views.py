from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from .models import Academic
from .forms import AcademicProfileForm


def academic_profile(request, academic_id):
    """ view to show individual article details """
    academic = get_object_or_404(Academic, pk=academic_id)

    if request.method == 'POST':
        form = AcademicProfileForm(request.POST, instance=academic)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated, {academic.name}')

    # academics = Academic.objects.all()
    followers = academic.academic_set.all().count()
    form = AcademicProfileForm(instance=academic)
    orders = academic.orders.all()

    context = {
        'academic': academic,
        'followers': followers,
        'form': form,
        'orders': orders,
    }

    return render(request, 'academics/academic_profile.html', context)
