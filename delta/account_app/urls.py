from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.account, name='account_app'),
    path('login/', auth_views.LoginView.as_view(template_name='account_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account_app/logout.html'), name='logout'),
]
