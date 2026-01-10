#!/bin/bash
# Enterprise Application Manager - Configuration Example
# Copy this file to manage.config.sh and customize for your environment

# Application Settings
APP_NAME="Enterprise Application Manager"
WEB_PORT=50478
MINIO_CONSOLE_PORT=9005
MINIO_API_PORT=9004

# Docker Settings
DOCKER_COMPOSE_FILE="docker-compose.yml"
WEB_CONTAINER="enterprise-app-web"
MINIO_CONTAINER="enterprise-app-minio"
NGINX_CONTAINER="enterprise-app-nginx"

# Database Settings
DB_FILE="data/db.sqlite3"
DB_BACKUP_DIR="backups/database"

# MinIO Settings
MINIO_BUCKET="enterprise-app-media"
MINIO_DATA_DIR="data/minio"
MINIO_CONSOLE_URL="http://localhost:9005"

# File Paths
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATIC_DIR="static"
STATICFILES_DIR="staticfiles"
MEDIA_DIR="media"
LOG_DIR="logs"
CERTS_DIR="certs"

# Environment File
ENV_FILE=".env"

# Development Settings
DEFAULT_BROWSER="open"  # macOS: "open", Linux: "xdg-open", Chrome: "google-chrome"
AUTO_OPEN_BROWSER=false
LOG_TAIL_LINES=100

# Backup Settings
BACKUP_ROOT="backups"
BACKUP_RETENTION=7
BACKUP_INCLUDE_MEDIA=true
BACKUP_INCLUDE_MINIO=true

# Migration Settings
MIGRATION_BATCH_SIZE=100  # Process files in batches
MIGRATION_VERIFY_CHECKSUM=true  # Verify with MD5
