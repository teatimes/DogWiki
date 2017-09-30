"""
WSGI config for dogwiki project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.prod_settings")
print("[WSGI] Using ", os.environ.get("DJANGO_SETTINGS_MODULE"))

application = get_wsgi_application()
