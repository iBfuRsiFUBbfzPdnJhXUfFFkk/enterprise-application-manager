from json import loads

from core.settings.common.environment import env

SECRET_KEY: str = env(var='DJANGO_SECRET_KEY')
ALLOWED_HOSTS: list[str] = loads(s=env(default='["127.0.0.1","localhost"]', var='ALLOWED_HOSTS'))

# CSRF Trusted Origins for HTTPS access
# Base origins that are always trusted
CSRF_TRUSTED_ORIGINS: list[str] = [
    'https://localhost',
    'https://127.0.0.1',
]

# Add extra origins from environment variable (e.g., for .local domain access)
# Format: comma-separated list of URLs like "https://hostname.local:50478,https://other-host:8443"
csrf_extra = env(default='', var='CSRF_TRUSTED_ORIGINS_EXTRA')
if csrf_extra:
    CSRF_TRUSTED_ORIGINS.extend([origin.strip() for origin in csrf_extra.split(',') if origin.strip()])

# Security headers
# X-Frame-Options: Allow same-origin framing (needed for PDF preview iframes)
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Default is 'DENY'

# Session and cookie settings
# Use unique cookie names to avoid conflicts when running multiple Django apps on localhost
SESSION_COOKIE_NAME: str = 'eam_sessionid'  # Default is 'sessionid'
CSRF_COOKIE_NAME: str = 'eam_csrftoken'  # Default is 'csrftoken'
LANGUAGE_COOKIE_NAME: str = 'eam_django_language'  # Default is 'django_language'
