from django.urls import path
from . import views_dashboard

urlpatterns = [
    path('posts/', views_dashboard.dashboard_post_list, name='dashboard_post_list'),
    path('posts/new/', views_dashboard.dashboard_post_create, name='dashboard_post_create'),
    path('posts/<int:post_id>/edit/', views_dashboard.dashboard_post_edit, name='dashboard_post_edit'),
    path('posts/<int:post_id>/delete/', views_dashboard.dashboard_post_delete, name='dashboard_post_delete'),
]
