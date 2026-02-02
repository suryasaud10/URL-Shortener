from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'), 
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path('create/', views.create_url, name='create_url'),
    path('create/custom/', views.create_custom_url, name='create_custom_url'),
    path('edit/<int:pk>/', views.edit_url, name='edit_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('qr/<int:pk>/', views.generate_qr, name='generate_qr'),
    path('<str:short_key>/', views.redirect_url, name='redirect_url'),
]