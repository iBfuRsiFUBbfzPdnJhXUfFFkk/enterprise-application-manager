#!/bin/bash
set -e

# Run MinIO bucket check in background (non-blocking)
(python manage.py check_minio_bucket --create-if-missing 2>/dev/null || true) &

# Copy Django admin static files only if missing
if [ ! -d "/app/static/admin" ]; then
    cp -r /usr/local/lib/python3.13/site-packages/django/contrib/admin/static/admin /app/static/ 2>/dev/null || true
fi

echo "Starting Django server..."
exec "$@"
