# User/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('reviews/', ReviewsListApi.as_view(), name='reviews'),
    path('reviews-overview/', ReviewsOverview.as_view(), name='reviews_overview'),
]
