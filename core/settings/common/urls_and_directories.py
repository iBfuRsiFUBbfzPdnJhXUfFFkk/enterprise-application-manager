from core.settings.common.environment import BASE_DIR, env

ROOT_URLCONF = 'core.urls'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/authenticated/'
LOGOUT_REDIRECT_URL = '/login/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
