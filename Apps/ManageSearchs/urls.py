# User/urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
    path('search/', SearchApi.as_view(), name='search_api'),
]
