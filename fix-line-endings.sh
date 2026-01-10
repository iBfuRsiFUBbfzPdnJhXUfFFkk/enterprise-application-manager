#!/bin/bash
# Fix Line Endings for Docker Compatibility
# This script fixes CRLF line endings that may have been checked out on Windows

set -e

echo -e "\033[0;36mFixing line endings for Docker compatibility...\033[0m"
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    echo -e "\033[0;31mError: Git is not installed or not in PATH\033[0m"
    exit 1
fi

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo -e "\033[0;31mError: Not in a git repository\033[0m"
    exit 1
fi

cd "$REPO_ROOT"

echo -e "\033[0;90mRepository root: $REPO_ROOT\033[0m"
echo ""

# Remove all files from git index
echo -e "\033[0;33mStep 1/3: Removing files from git index...\033[0m"
git rm --cached -r . >/dev/null 2>&1

# Reset the git index
echo -e "\033[0;33mStep 2/3: Resetting git index...\033[0m"
git reset --hard >/dev/null 2>&1

# Renormalize line endings according to .gitattributes
echo -e "\033[0;33mStep 3/3: Renormalizing line endings...\033[0m"
git add --renormalize . >/dev/null 2>&1

echo ""
echo -e "\033[0;32m✓ Line endings fixed!\033[0m"
echo ""
echo -e "\033[0;90mFiles have been normalized according to .gitattributes:\033[0m"
echo -e "\033[0;90m  • Shell scripts (.sh) -> LF (Unix)\033[0m"
echo -e "\033[0;90m  • Docker files -> LF (Unix)\033[0m"
echo -e "\033[0;90m  • PowerShell scripts (.ps1) -> CRLF (Windows)\033[0m"
echo ""

# Check if there are any changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "\033[0;33mThe following files were normalized:\033[0m"
    git status --short
    echo ""
    echo -e "\033[0;36mYou can commit these changes with:\033[0m"
    echo -e "\033[0;90m  git commit -m 'chore: normalize line endings'\033[0m"
else
    echo -e "\033[0;32mNo files needed normalization. All files already have correct line endings.\033[0m"
fi

echo ""
echo -e "\033[0;36mYou can now rebuild your Docker containers:\033[0m"
echo -e "\033[0;90m  docker compose down\033[0m"
echo -e "\033[0;90m  docker compose up --build\033[0m"
echo ""
