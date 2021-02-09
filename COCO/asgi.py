import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "COCO.settings")
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from Apps.ManageNotifications.routing import websocket_urlpatterns as notify_ws
from Apps.ManageChats.routing import websocket_urlpatterns as chats_ws

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notify_ws +
            chats_ws
        )
    ),

})
