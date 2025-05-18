import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # Chat uygulamasının routing.py dosyasını içe aktar

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(chat.routing.websocket_urlpatterns)  # WebSocket yönlendirmesini burada ekliyoruz
        ),
    }
)
