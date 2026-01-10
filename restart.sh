#!/bin/bash

# Quick Restart Docker Containers
# This script simply restarts all containers without rebuilding

set -e  # Exit on error

echo "=========================================="
echo "Restarting Docker Services"
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

echo "Restarting all containers..."
$DOCKER_CMD restart

echo ""
echo "=========================================="
echo "Restart complete!"
echo "=========================================="
echo ""
echo "Services are now running. Check status with:"
echo "  $DOCKER_CMD ps"
echo ""
echo "View logs with:"
echo "  $DOCKER_CMD logs -f"
echo ""
