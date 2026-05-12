"""
lostfound/wsgi.py
Gunicorn on Render will use this as the entry point.
DJANGO_SETTINGS_MODULE should be set as an env var on Render:
  DJANGO_SETTINGS_MODULE=lostfound.settings.production
This fallback ensures production is chosen when running on Render
even if the env var is missing.
"""
import os
from django.core.wsgi import get_wsgi_application

# If DJANGO_SETTINGS_MODULE is already set (by Render env var), use it.
# Otherwise auto-detect: Render sets the RENDER env var.
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    if os.environ.get('RENDER'):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'lostfound.settings.production'
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'lostfound.settings.development'

application = get_wsgi_application()
