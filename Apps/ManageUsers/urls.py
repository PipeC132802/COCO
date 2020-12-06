# User/urls.py
from django.urls import path, include

from .views import *
from rest_framework.authtoken import views

urlpatterns = [
    path('user-auth/', include('dj_rest_auth.urls')),
    path('token-auth/', views.obtain_auth_token, name='token_auth'),
    path('user-logout/', LogoutApi.as_view(), name='user_logout'),
    path('user-status/', UserStatus.as_view(), name='user_status')
]