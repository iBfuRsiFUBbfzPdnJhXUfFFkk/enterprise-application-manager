from core.settings.common.environment import BASE_DIR, env

ROOT_URLCONF = 'core.urls'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/authenticated/'
LOGOUT_REDIRECT_URL = '/login/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Poppler path for PDF to image conversion (optional)
# On Windows: Set to the bin directory, e.g., "C:/Program Files/poppler/bin"
# On Unix/Mac: Leave empty to use system PATH
POPPLER_PATH = env.str(default=None, var='POPPLER_PATH')
