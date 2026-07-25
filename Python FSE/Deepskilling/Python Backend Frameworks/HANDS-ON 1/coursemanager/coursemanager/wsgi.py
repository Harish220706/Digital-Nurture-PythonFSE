"""
WSGI config for coursemanager project.
WSGI (Web Server Gateway Interface) is the traditional, synchronous
interface Django uses by default for standard HTTP request/response apps.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
application = get_wsgi_application()
