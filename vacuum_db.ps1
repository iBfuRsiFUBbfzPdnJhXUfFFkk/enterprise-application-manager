# PowerShell script to vacuum the SQLite database
# This reclaims unused space and optimizes the database file

$ErrorActionPreference = "Stop"

$DB_FILE = "db.sqlite3"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$DB_PATH = Join-Path $SCRIPT_DIR $DB_FILE

# Check if database file exists
if (-not (Test-Path $DB_PATH)) {
    Write-Host "Error: Database file not found at $DB_PATH" -ForegroundColor Red
    exit 1
}

# Check if sqlite3 command is available
$sqlite3Path = $null
try {
    $sqlite3Path = Get-Command sqlite3 -ErrorAction Stop | Select-Object -ExpandProperty Source
} catch {
    Write-Host "Error: sqlite3 command not found. Please install SQLite." -ForegroundColor Red
    Write-Host "Download from: https://www.sqlite.org/download.html" -ForegroundColor Yellow
    exit 1
}

Write-Host "Database VACUUM Utility" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Get size before vacuum
$fileInfo = Get-Item $DB_PATH
$sizeBefore = $fileInfo.Length
$sizeBeforeMB = [math]::Round($sizeBefore / 1MB, 2)

Write-Host "Database: $DB_PATH"
Write-Host "Size before VACUUM: $sizeBeforeMB MB ($sizeBefore bytes)"
Write-Host ""
Write-Host "Running VACUUM..." -ForegroundColor Yellow

# Run VACUUM command
try {
    & sqlite3 $DB_PATH "VACUUM;"
} catch {
    Write-Host "Error running VACUUM: $_" -ForegroundColor Red
    exit 1
}

# Get size after vacuum
$fileInfo = Get-Item $DB_PATH
$sizeAfter = $fileInfo.Length
$sizeAfterMB = [math]::Round($sizeAfter / 1MB, 2)

# Calculate space freed
$spaceFreed = $sizeBefore - $sizeAfter
$spaceFreedMB = [math]::Round($spaceFreed / 1MB, 2)

# Calculate percentage
if ($sizeBefore -gt 0) {
    $percentFreed = [math]::Round(($spaceFreed / $sizeBefore) * 100, 2)
} else {
    $percentFreed = 0
}

Write-Host "VACUUM completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Size after VACUUM: $sizeAfterMB MB ($sizeAfter bytes)"
Write-Host "Space freed: $spaceFreedMB MB ($spaceFreed bytes)" -ForegroundColor Green
Write-Host "Reduction: $percentFreed%" -ForegroundColor Green
