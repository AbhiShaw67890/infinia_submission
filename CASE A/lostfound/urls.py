"""
lostfound/urls.py — Root URL configuration.
Each app has its own urls.py for clean separation.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),           # home feed
    path('accounts/', include('accounts.urls')),
    path('items/', include('items.urls')),
    path('claims/', include('claims.urls')),
]
