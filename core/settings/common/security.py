from json import loads

from core.settings.common.environment import env

SECRET_KEY: str = env(var='DJANGO_SECRET_KEY')
ALLOWED_HOSTS: list[str] = loads(s=env(default='["127.0.0.1","localhost"]', var='ALLOWED_HOSTS'))
