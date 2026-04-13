"""
ASGI config for iet_24782037_2026 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / '24782037_iet_2026'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iet_24782037_2026.settings')

application = get_asgi_application()
