# myproject/asgi.py

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from main import consumers
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [path('ws/', consumers.VideoConsumer.as_asgi())],
        )
    ),
})
