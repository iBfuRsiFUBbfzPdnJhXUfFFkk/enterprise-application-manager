"""
Logging configuration for Django application.

Configures logging for encryption operations and other application components.
"""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
LOGS_DIR = BASE_DIR / 'logs'

# Ensure logs directory exists
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'encryption': {
            'format': '{levelname} {asctime} [ENCRYPTION] {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'encryption_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOGS_DIR / 'encryption.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'encryption',
        },
        'application_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOGS_DIR / 'application.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOGS_DIR / 'errors.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Encryption-specific logger
        'core.utilities.encryption': {
            'handlers': ['encryption_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'core.utilities.encryption_health_check': {
            'handlers': ['encryption_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'core.forms.common.generic_encrypted_save': {
            'handlers': ['encryption_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Django core loggers
        'django': {
            'handlers': ['console', 'application_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['error_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        # Application logger (root logger for core app)
        'core': {
            'handlers': ['application_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'application_file'],
        'level': 'INFO',
    },
}

# In development, use DEBUG level for console output
if os.getenv('DEBUG', 'False').lower() == 'true':
    LOGGING['handlers']['console']['level'] = 'DEBUG'
    LOGGING['loggers']['core.utilities.encryption']['level'] = 'DEBUG'
    LOGGING['loggers']['core']['level'] = 'DEBUG'
    LOGGING['root']['level'] = 'DEBUG'
