#!/bin/bash
set -e

echo "Checking MinIO bucket..."
python manage.py check_minio_bucket --create-if-missing || echo "⚠ MinIO bucket check skipped (MinIO may not be ready yet)"

echo "Starting Django server..."
exec "$@"
