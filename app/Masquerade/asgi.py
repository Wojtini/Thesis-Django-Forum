"""
ASGI config for Masquerade project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

import sys
import pathlib


sys.path.append(str(pathlib.Path(__file__).parent.resolve()))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Masquerade.settings")

application = get_asgi_application()
