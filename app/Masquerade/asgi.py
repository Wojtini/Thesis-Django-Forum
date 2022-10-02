"""
ASGI config for Masquerade project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import sys
import pathlib
import forum.routing

sys.path.append(str(pathlib.Path(__file__).parent.resolve()))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Masquerade.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                forum.routing.websocket_urlpatterns
            )
        )
    ),
})
