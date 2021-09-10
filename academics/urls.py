from django.urls import path
from . import views

urlpatterns = [
    path('<academic_id>', views.academic_profile, name='academic_profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    path('<int:article_id>/', views.article_detail_profile, name='article_detail_profile'),
]
