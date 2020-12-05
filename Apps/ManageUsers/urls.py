# User/urls.py
from django.urls import path

from .views import *
from rest_framework.authtoken import views

urlpatterns = [
    path('token-auth/', views.obtain_auth_token, name='token_auth')
]