from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer, ChatConsumerCrm
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "royalflowers.settings")
# Инициализируйте приложение Django ASGI заранее, чтобы обеспечить заполнение AppRegistry перед импортом кода, который может импортировать модели ORM.

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Приложение Django ASGI для обработки традиционных HTTP-запросов
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("api/chat/", ChatConsumer.as_asgi()),
            path("api/chat_crm/", ChatConsumerCrm.as_asgi()),
        ])
    ),
})