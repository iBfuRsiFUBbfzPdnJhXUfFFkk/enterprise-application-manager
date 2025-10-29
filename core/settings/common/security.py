from json import loads

from core.settings.common.environment import env

SECRET_KEY: str = env(var='DJANGO_SECRET_KEY')
ALLOWED_HOSTS: list[str] = loads(s=env(default='["127.0.0.1","localhost"]', var='ALLOWED_HOSTS'))

# Session and cookie settings
# Use unique cookie names to avoid conflicts when running multiple Django apps on localhost
SESSION_COOKIE_NAME: str = 'eam_sessionid'  # Default is 'sessionid'
CSRF_COOKIE_NAME: str = 'eam_csrftoken'  # Default is 'csrftoken'
LANGUAGE_COOKIE_NAME: str = 'eam_django_language'  # Default is 'django_language'
