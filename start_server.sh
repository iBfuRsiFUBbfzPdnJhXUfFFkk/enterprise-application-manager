#!/bin/bash

# Enterprise Application Manager - Server Startup Script
# This script performs pre-flight checks and starts the Django development server

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Enterprise Application Manager${NC}"
echo -e "${BLUE}Server Startup Script${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}Error: Virtual environment not found at .venv${NC}"
    echo "Please create a virtual environment first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Please create a .env file with required environment variables."
    echo "See .documentation/environment-setup.md for details."
    exit 1
fi

# Set Django settings module (default to local if not set)
if [ -z "$DJANGO_SETTINGS_MODULE" ]; then
    export DJANGO_SETTINGS_MODULE="core.settings.local"
    echo -e "${YELLOW}DJANGO_SETTINGS_MODULE not set, using: core.settings.local${NC}"
else
    echo -e "${GREEN}Using DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}[1/5] Activating virtual environment...${NC}"
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Check for pending migrations
echo -e "${BLUE}[2/5] Checking for pending migrations...${NC}"
if .venv/bin/python manage.py showmigrations --plan | grep -q "\[ \]"; then
    echo -e "${YELLOW}Pending migrations found. Running migrations...${NC}"
    .venv/bin/python manage.py migrate
    echo -e "${GREEN}✓ Migrations completed${NC}"
else
    echo -e "${GREEN}✓ No pending migrations${NC}"
fi
echo ""

# Collect static files (only in non-DEBUG mode)
echo -e "${BLUE}[3/5] Checking static files...${NC}"
# Skip static files collection in local development (DEBUG=True)
echo -e "${YELLOW}Skipping static files collection (development mode)${NC}"
echo ""

# Check for missing migrations
echo -e "${BLUE}[4/5] Checking for model changes...${NC}"
if .venv/bin/python manage.py makemigrations --dry-run --check > /dev/null 2>&1; then
    echo -e "${GREEN}✓ No model changes detected${NC}"
else
    echo -e "${YELLOW}Warning: Model changes detected but no migrations created${NC}"
    echo "Run 'python manage.py makemigrations' to create migrations"
fi
echo ""

# Start the development server
echo -e "${BLUE}[5/5] Starting development server...${NC}"
echo -e "${GREEN}✓ Server starting at http://127.0.0.1:50478/${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

.venv/bin/python manage.py runserver 50478
