"""
WSGI config for onlineCAL project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineCAL.settings')

application = get_wsgi_application()
if os.path.exists(ENV_LOCATION):
    load_dotenv(ENV_LOCATION)
