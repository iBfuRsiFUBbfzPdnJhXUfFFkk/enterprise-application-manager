"""
URL patterns for health check endpoints.
"""

from django.urls import path

from core.views.health.encryption_health_view import encryption_health_view

urlpatterns = [
    path('encryption/', encryption_health_view, name='health_encryption'),
]
