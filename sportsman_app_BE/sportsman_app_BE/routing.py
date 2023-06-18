from os import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from sportsman.consumers import SocketConsumer

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                [
                    path('http://localhost:3000/socket.io/',
                         SocketConsumer.as_asgi()),
                ]
            )
        ),
    }
)
