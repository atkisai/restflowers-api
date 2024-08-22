from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer
from app.consumers import AppConsumer


application = ProtocolTypeRouter({

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("chat/", ChatConsumer),
            path("app/", AppConsumer),
        ])
    ),
})