from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

#from Apps.ManageChats import routing as chat_routing
from Apps.ManageNotifications import routing as notify_routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            #chat_routing.websocket_urlpatterns +
            notify_routing.websocket_urlpatterns

        ),
    ),
})