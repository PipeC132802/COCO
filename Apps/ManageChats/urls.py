# User/urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
    path('inbox/', ChatsListApi.as_view(), name='inbox'),
    path('messages/', MessagesApi.as_view(), name='inbox'),
    path('unread-messages/', UnreadMsgsApi.as_view(), name='inbox'),

]
