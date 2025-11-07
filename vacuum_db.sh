#!/bin/bash

# Script to vacuum the SQLite database
# This reclaims unused space and optimizes the database file

set -e  # Exit on error

DB_FILE="db.sqlite3"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="${SCRIPT_DIR}/${DB_FILE}"

# Check if database file exists
if [ ! -f "$DB_PATH" ]; then
    echo "Error: Database file not found at ${DB_PATH}"
    exit 1
fi

# Check if sqlite3 command is available
if ! command -v sqlite3 &> /dev/null; then
    echo "Error: sqlite3 command not found. Please install SQLite."
    exit 1
fi

echo "Database VACUUM Utility"
echo "======================"
echo ""

# Get size before vacuum
SIZE_BEFORE=$(stat -f%z "$DB_PATH" 2>/dev/null || stat -c%s "$DB_PATH" 2>/dev/null)
SIZE_BEFORE_MB=$(echo "scale=2; $SIZE_BEFORE / 1024 / 1024" | bc)

echo "Database: ${DB_PATH}"
echo "Size before VACUUM: ${SIZE_BEFORE_MB} MB (${SIZE_BEFORE} bytes)"
echo ""
echo "Running VACUUM..."

# Run VACUUM command
sqlite3 "$DB_PATH" "VACUUM;"

# Get size after vacuum
SIZE_AFTER=$(stat -f%z "$DB_PATH" 2>/dev/null || stat -c%s "$DB_PATH" 2>/dev/null)
SIZE_AFTER_MB=$(echo "scale=2; $SIZE_AFTER / 1024 / 1024" | bc)

# Calculate space freed
SPACE_FREED=$((SIZE_BEFORE - SIZE_AFTER))
SPACE_FREED_MB=$(echo "scale=2; $SPACE_FREED / 1024 / 1024" | bc)

# Calculate percentage
if [ $SIZE_BEFORE -gt 0 ]; then
    PERCENT_FREED=$(echo "scale=2; $SPACE_FREED * 100 / $SIZE_BEFORE" | bc)
else
    PERCENT_FREED=0
fi

echo "VACUUM completed successfully!"
echo ""
echo "Size after VACUUM: ${SIZE_AFTER_MB} MB (${SIZE_AFTER} bytes)"
echo "Space freed: ${SPACE_FREED_MB} MB (${SPACE_FREED} bytes)"
echo "Reduction: ${PERCENT_FREED}%"
