"""
production.py — Settings for Render deployment.

Required environment variables on Render:
  DJANGO_SETTINGS_MODULE = lostfound.settings.production
  SECRET_KEY             = <generate a new strong key>
  DATABASE_URL           = <your neon postgresql url>
  CLOUDINARY_CLOUD_NAME  = dm5mmxgpv
  CLOUDINARY_API_KEY     = 818832683144922
  CLOUDINARY_API_SECRET  = iIxSt_hdMOhv5I6SDKw9VAsKtRw
  ALLOWED_HOSTS          = findit-xgpm.onrender.com
  DEBUG                  = False
"""

import os
from .base import *
from decouple import config

DEBUG = False

# ── ALLOWED_HOSTS ─────────────────────────────────────────────────────────────
# Build the list from multiple sources so it always works on Render:
#   1. ALLOWED_HOSTS env var (comma-separated)
#   2. RENDER_EXTERNAL_HOSTNAME env var (auto-set by Render)
#   3. Hard-coded Render domain as a final fallback

_hosts = config('ALLOWED_HOSTS', default='').split(',')
_hosts = [h.strip() for h in _hosts if h.strip()]

# Render automatically sets RENDER_EXTERNAL_HOSTNAME to your service URL
_render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
if _render_hostname and _render_hostname not in _hosts:
    _hosts.append(_render_hostname)

# Hard-coded fallback — always allow our known Render domain
_known = 'findit-xgpm.onrender.com'
if _known not in _hosts:
    _hosts.append(_known)

ALLOWED_HOSTS = _hosts

# Also set CSRF_TRUSTED_ORIGINS so POST forms work over HTTPS on Render
CSRF_TRUSTED_ORIGINS = [f'https://{h}' for h in ALLOWED_HOSTS if h]

# ── SECURITY ──────────────────────────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER    = True
SECURE_CONTENT_TYPE_NOSNIFF  = True
X_FRAME_OPTIONS              = 'DENY'
SECURE_SSL_REDIRECT          = True
SESSION_COOKIE_SECURE        = True
CSRF_COOKIE_SECURE           = True
SECURE_HSTS_SECONDS          = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
