"""
Simple health check view for Docker container startup verification.

This view is intentionally unauthenticated to allow Docker health checks
to work before users log in.
"""

from django.http import HttpResponse


def startup_health_view(request):
    """Return a simple 200 OK response for health checks."""
    return HttpResponse("OK", content_type="text/plain")
