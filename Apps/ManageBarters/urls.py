# User/urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
    path('barter/', BarterApi.as_view(), name='barter'),
    path('barter-list/', BarterListApi.as_view(), name='barter_list'),
    path('barter-reactions/', BarterReactionsApi.as_view(), name='barter_reactions'),
    path('create-barter-reaction/', CreateBarterReactionApi.as_view(), name='barter_reaction'),
]
