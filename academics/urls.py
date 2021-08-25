from django.urls import path
from . import views

urlpatterns = [
    path('<academic_id>', views.academic_profile, name='academic_profile'),
]
