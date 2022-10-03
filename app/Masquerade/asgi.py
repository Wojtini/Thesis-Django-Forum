import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import sys
import pathlib

import forum.routing_urls

sys.path.append(str(pathlib.Path(__file__).parent.resolve()))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Masquerade.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                forum.routing_urls.websocket_urlpatterns,
            )
        )
    ),
})
