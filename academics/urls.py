from django.urls import path
from . import views

urlpatterns = [
    path('<int:academic_id>', views.academic_profile, name='academic_profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    path('<int:article_id>/', views.article_detail_profile, name='article_detail_profile'),
    path('profile/<int:academic_id>/', views.academic_profile_from_profile, name='academic_profile_from_profile'),
    path('follow/<int:academic_id>', views.follow, name='follow'),
    path('unfollow/<int:academic_id>', views.unfollow, name='unfollow'),
    path('unfollow_from_hub/<int:academic_id>', views.unfollow_from_hub, name='unfollow_from_hub'),
]
