"""
ASGI config for coursemanager project.
ASGI (Asynchronous Server Gateway Interface) supports async views,
WebSockets, and long-lived connections. Switch to ASGI (with an ASGI
server like uvicorn/daphne) when you need async views or channels.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
application = get_asgi_application()
