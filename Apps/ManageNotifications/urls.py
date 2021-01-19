# User/urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
    path('notifications/', NotificationsListApi.as_view(), name='notification_list'),
]
