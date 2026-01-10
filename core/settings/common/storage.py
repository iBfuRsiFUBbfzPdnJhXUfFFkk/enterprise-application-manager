"""
Storage backend configuration for MinIO object storage.

This module configures Django to use either MinIO S3-compatible storage
or local filesystem storage based on the USE_MINIO environment variable.
"""

import os
from core.settings.common.environment import env, BASE_DIR

# Storage backend selection
USE_MINIO = env.bool('USE_MINIO', default=False)

if USE_MINIO:
    # MinIO credentials and configuration
    AWS_ACCESS_KEY_ID = env.str('MINIO_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = env.str('MINIO_SECRET_KEY')
    AWS_STORAGE_BUCKET_NAME = env.str('MINIO_BUCKET_NAME', default='enterprise-app-media')

    # MinIO endpoint (internal Docker service name or external URL)
    MINIO_ENDPOINT = env.str('MINIO_ENDPOINT', default='minio:9000')
    AWS_S3_ENDPOINT_URL = f"http://{MINIO_ENDPOINT}"

    # SSL configuration
    AWS_S3_USE_SSL = env.bool('MINIO_USE_SSL', default=False)

    # MinIO/S3 settings
    AWS_S3_REGION_NAME = 'us-east-1'  # MinIO doesn't care but boto3 requires it
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_FILE_OVERWRITE = False  # Don't overwrite files with same name
    AWS_DEFAULT_ACL = None  # Use bucket's default ACL
    AWS_QUERYSTRING_AUTH = True  # Generate signed URLs
    AWS_QUERYSTRING_EXPIRE = 3600  # Signed URLs expire after 1 hour

    # Django 4.2+ STORAGES setting (replaces DEFAULT_FILE_STORAGE)
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    # Legacy setting for backwards compatibility
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

else:
    # Local file storage (legacy/development)
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
