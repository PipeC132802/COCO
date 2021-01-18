import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from Apps.ManageNotifications.routing import websocket_urlpatterns as notify_ws

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'COCO.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            notify_ws
        )
    ),
})