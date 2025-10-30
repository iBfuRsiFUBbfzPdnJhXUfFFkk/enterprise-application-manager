from django.db.models import F
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from core.models.link import Link


def link_short_redirect_view(request: HttpRequest, short_code: str) -> HttpResponseRedirect:
    """
    Public redirect view for short URLs.

    Redirects to the full URL and tracks analytics (click count, timestamps).
    This view is PUBLIC and does not require authentication.

    Args:
        request: HttpRequest object
        short_code: The short code from the URL (e.g., 'abc123xyz0')

    Returns:
        HttpResponseRedirect to the full URL

    Raises:
        Http404: If short_code doesn't exist or link is inactive
    """
    # Get the link by short_code (case-insensitive) where short URL is active
    link = get_object_or_404(
        Link,
        short_code__iexact=short_code,
        is_short_url_active=True
    )

    # Update analytics atomically
    now = timezone.now()

    # Increment click count using F() expression for atomic update
    Link.objects.filter(id=link.id).update(
        click_count=F('click_count') + 1,
        last_accessed_at=now
    )

    # Set first_accessed_at if this is the first click
    if link.first_accessed_at is None:
        Link.objects.filter(id=link.id).update(first_accessed_at=now)

    # Redirect to the actual URL (permanent redirect = 301)
    # Using 301 for SEO benefits and browser caching
    return HttpResponseRedirect(redirect_to=link.url)
