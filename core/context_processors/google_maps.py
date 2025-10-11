"""
Context processor for Google Maps API key.

This makes the Google Maps API key available in all templates
as `google_maps_api_key` if it's configured in ThisServerConfiguration.
"""

from core.models.this_server_configuration import ThisServerConfiguration


def google_maps_api_key(request):
    """
    Add Google Maps API key to template context.

    Returns:
        dict: Dictionary with 'google_maps_api_key' key containing the decrypted API key or None
    """
    try:
        config = ThisServerConfiguration.current()
        api_key = config.google_maps_api_key_decrypted if config else None
        return {
            'google_maps_api_key': api_key,
            'google_maps_enabled': api_key is not None and len(api_key) > 0
        }
    except Exception as e:
        # If there's any error, return None to gracefully degrade
        print(f"Error fetching Google Maps API key: {e}")
        return {
            'google_maps_api_key': None,
            'google_maps_enabled': False
        }
