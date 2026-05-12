"""
This file exists only to redirect to the correct settings package.
Render (and any tool that defaults to 'lostfound.settings') will import this,
which immediately imports production settings.

Set DJANGO_SETTINGS_MODULE=lostfound.settings.production in Render env vars
to use production.py directly (preferred). This file is a fallback safety net.
"""
# Detect if we're running on Render (production) or locally (development)
import os

if os.environ.get('RENDER'):
    from lostfound.settings.production import *
else:
    from lostfound.settings.development import *
