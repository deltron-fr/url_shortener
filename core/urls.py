"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from url_shortener import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('urls/shorten/', views.ShortURLCreateAPIView.as_view(), name='shorten-url'),
    path('register/', views.CreateUserAPIView.as_view(), name='register-user'),
    path('login/', views.LoginView.as_view(), name='login-user'),
    path('api-auth/', include('rest_framework.urls')),
    path('logout/', views.LogoutView.as_view(), name='logout-user'),
    path('health/', views.HealthView.as_view(), name='application-health'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('urls/<int:pk>', views.URLDetailAPIView.as_view(), name='delete-user'),
    path('<str:short_code>/', views.RedirectAPIView.as_view(), name='redirect-original')
]
