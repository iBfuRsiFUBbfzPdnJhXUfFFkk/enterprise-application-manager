#!/usr/bin/env pwsh
# Fix Line Endings for Docker Compatibility
# This script fixes CRLF line endings that may have been checked out on Windows

Write-Host "Fixing line endings for Docker compatibility..." -ForegroundColor Cyan
Write-Host ""

# Check if git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Git is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Get repository root
$repoRoot = git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) {
    Write-Host "Error: Not in a git repository" -ForegroundColor Red
    exit 1
}

Set-Location $repoRoot

Write-Host "Repository root: $repoRoot" -ForegroundColor Gray
Write-Host ""

# Remove all files from git index
Write-Host "Step 1/3: Removing files from git index..." -ForegroundColor Yellow
git rm --cached -r . 2>&1 | Out-Null

# Reset the git index
Write-Host "Step 2/3: Resetting git index..." -ForegroundColor Yellow
git reset --hard 2>&1 | Out-Null

# Renormalize line endings according to .gitattributes
Write-Host "Step 3/3: Renormalizing line endings..." -ForegroundColor Yellow
git add --renormalize . 2>&1 | Out-Null

Write-Host ""
Write-Host "✓ Line endings fixed!" -ForegroundColor Green
Write-Host ""
Write-Host "Files have been normalized according to .gitattributes:" -ForegroundColor Gray
Write-Host "  • Shell scripts (.sh) -> LF (Unix)" -ForegroundColor Gray
Write-Host "  • Docker files -> LF (Unix)" -ForegroundColor Gray
Write-Host "  • PowerShell scripts (.ps1) -> CRLF (Windows)" -ForegroundColor Gray
Write-Host ""

# Check if there are any changes
$status = git status --porcelain
if ($status) {
    Write-Host "The following files were normalized:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    Write-Host "You can commit these changes with:" -ForegroundColor Cyan
    Write-Host "  git commit -m 'chore: normalize line endings'" -ForegroundColor Gray
} else {
    Write-Host "No files needed normalization. All files already have correct line endings." -ForegroundColor Green
}

Write-Host ""
Write-Host "You can now rebuild your Docker containers:" -ForegroundColor Cyan
Write-Host "  docker compose down" -ForegroundColor Gray
Write-Host "  docker compose up --build" -ForegroundColor Gray
Write-Host ""
