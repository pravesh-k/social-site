from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),     # previous login view w/o using Django auth views
    path('login/', auth_views.LoginView.as_view(), name='login'),       #LoginView refers to the html files located 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    #inside templates/registration by default
    path('', views.dashboard, name='dashboard'),
    ]