#!/bin/bash
set -e

echo "Building Tailwind CSS..."
npm run build:css
if [ $? -eq 0 ]; then
    echo "✓ Tailwind CSS built successfully"
else
    echo "✗ Tailwind CSS build failed - check for errors"
fi

echo "Checking MinIO bucket..."
python manage.py check_minio_bucket --create-if-missing || echo "⚠ MinIO bucket check skipped (MinIO may not be ready yet)"

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Starting Django server..."
exec "$@"
