#!/bin/bash
# Local development server runner for Enterprise Application Manager

# Set Django settings to local environment
export DJANGO_SETTINGS_MODULE="core.settings.local"

# Clear Python bytecode cache for clean startup
echo "Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found at .venv/"
    echo "Please create the virtual environment first."
    exit 1
fi

# Run the development server
echo "Starting Django development server..."
echo "Settings: $DJANGO_SETTINGS_MODULE"
echo "Access the application at: http://127.0.0.1:50478"
echo ""

.venv/bin/python manage.py runserver 50478
