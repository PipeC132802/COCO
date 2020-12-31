# User/urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
    path('barter-api/', BarterApi.as_view(), name='barter'),
    path('barter-list-api/', BarterListApi.as_view(), name='barter_list'),
]
