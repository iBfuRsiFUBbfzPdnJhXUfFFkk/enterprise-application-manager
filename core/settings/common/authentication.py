from core.settings.common.ldap import BACKEND_BUILDER

AUTH_USER_MODEL = 'core.User'

AUTHENTICATION_BACKENDS = [
    'core.backends.passkey_backend.PasskeyBackend',
    *BACKEND_BUILDER,
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
