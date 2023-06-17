from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/my-endpoint/$', consumers.MyConsumer.as_asgi()),
    # Add more URL patterns for different WebSocket endpoints/consumers
]
