#!/bin/bash
set -e

echo "Checking MinIO bucket..."
python manage.py check_minio_bucket --create-if-missing || echo "⚠ MinIO bucket check skipped (MinIO may not be ready yet)"

# Copy Django admin static files if not present (for nginx to serve)
if [ ! -d "/app/static/admin" ]; then
    echo "Copying Django admin static files..."
    cp -r /usr/local/lib/python3.13/site-packages/django/contrib/admin/static/admin /app/static/
fi

echo "Starting Django server..."
exec "$@"
