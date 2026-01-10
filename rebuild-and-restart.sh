#!/bin/bash

# Rebuild and Restart Docker Containers
# This script stops containers, rebuilds images with no cache, and restarts everything

set -e  # Exit on error

echo "=========================================="
echo "Rebuilding and Restarting Docker Services"
echo "=========================================="
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
    echo "Error: Neither docker-compose nor docker command found"
    echo "Please install Docker and Docker Compose"
    exit 1
fi

# Determine which command to use
if command -v docker-compose &> /dev/null; then
    DOCKER_CMD="docker-compose"
else
    DOCKER_CMD="docker compose"
fi

echo "Step 1: Stopping all running containers..."
$DOCKER_CMD down

echo ""
echo "Step 2: Removing old images (optional cleanup)..."
read -p "Do you want to remove old images? This will free up disk space. (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    $DOCKER_CMD down --rmi local
    echo "Old images removed"
else
    echo "Skipping image removal"
fi

echo ""
echo "Step 3: Rebuilding images with no cache..."
$DOCKER_CMD build --no-cache

echo ""
echo "Step 4: Starting all services..."
$DOCKER_CMD up -d

echo ""
echo "=========================================="
echo "Rebuild and restart complete!"
echo "=========================================="
echo ""
echo "Services are now running. Check status with:"
echo "  $DOCKER_CMD ps"
echo ""
echo "View logs with:"
echo "  $DOCKER_CMD logs -f"
echo ""
