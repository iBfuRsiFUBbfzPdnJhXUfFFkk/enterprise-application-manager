from urllib.parse import urlparse

from django import template

register = template.Library()


@register.filter
def get_favicon_url(url: str, size: int = 32) -> str:
    """
    Extract domain from URL and return Google's favicon service URL.

    Args:
        url: The full URL (e.g., "https://github.com/user/repo")
        size: Icon size in pixels (default: 32)

    Returns:
        URL to the favicon image
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path

        # Use Google's favicon service
        return f"https://www.google.com/s2/favicons?domain={domain}&sz={size}"
    except Exception:
        # Fallback to a default icon
        return ""


@register.filter
def get_domain(url: str) -> str:
    """
    Extract domain from URL for display.

    Args:
        url: The full URL (e.g., "https://github.com/user/repo")

    Returns:
        Just the domain (e.g., "github.com")
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc or parsed.path
    except Exception:
        return url
