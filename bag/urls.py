from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_bag, name='bag'),
    path('add/<article_id>/', views.add_to_bag, name='add_to_bag'),
]
