# User/urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
    path('user-auth/', include('dj_rest_auth.urls')),
    path('create-user/', CreateUserApi.as_view(), name='create_user'),
    path('user-status/', UserStatus.as_view(), name='user_status'),
    path('confirm-user', ResetUserPasswordApi.as_view(), name='confirm_user')
]
