from django.urls import re_path
from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<username>\w+)/$', consumers.NotificationConsumer.as_asgi()),
]
