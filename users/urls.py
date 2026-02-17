from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users/register/', views.register, name='register'),
    path('api/v1/users/confirm/', views.confirm_user, name='confirm'),
    path('api/v1/users/login/', views.login_view, name='login'),
    path('api/v1/users/logout/', views.logout_view, name='logout'),
    path('api/v1/users/profile/', views.profile, name='profile'),
]