"""
URL patterns for health check endpoints.

Public health endpoints (no auth required):
- /health/startup/ - Docker container health check

Authenticated health endpoints (require login):
- /authenticated/health/encryption/ - Encryption system health check
"""

from django.urls import path

from core.views.health.encryption_health_view import encryption_health_view
from core.views.health.startup_health_view import startup_health_view

urlpatterns_health_public = [
    path('startup/', startup_health_view, name='health_startup'),
]

urlpatterns_health_authenticated = [
    path('encryption/', encryption_health_view, name='health_encryption'),
]

# Backwards compatibility alias
urlpatterns = urlpatterns_health_authenticated
