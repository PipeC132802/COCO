# User/urls.py
from django.urls import path, include
from .views import *
from rest_framework.authtoken import views

urlpatterns = [
    path('user-auth/', include('dj_rest_auth.urls')),
    path('create-user/', CreateUserApi.as_view(), name='create_user'),
    path('user-status/', UserStatus.as_view(), name='user_status')
]
