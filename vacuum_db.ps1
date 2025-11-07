# PowerShell script to vacuum the SQLite database
# This reclaims unused space and optimizes the database file

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false, HelpMessage="Path to sqlite3.exe executable")]
    [string]$Sqlite3Path
)

$ErrorActionPreference = "Stop"

$DB_FILE = "db.sqlite3"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$DB_PATH = Join-Path $SCRIPT_DIR $DB_FILE

# Check if database file exists
if (-not (Test-Path $DB_PATH)) {
    Write-Host "Error: Database file not found at $DB_PATH" -ForegroundColor Red
    exit 1
}

# Determine sqlite3 path
$sqlite3Exe = $null

if ($Sqlite3Path) {
    # Use provided path
    if (-not (Test-Path $Sqlite3Path)) {
        Write-Host "Error: sqlite3 executable not found at specified path: $Sqlite3Path" -ForegroundColor Red
        exit 1
    }
    $sqlite3Exe = $Sqlite3Path
    Write-Host "Using sqlite3 from: $sqlite3Exe" -ForegroundColor Yellow
    Write-Host ""
} else {
    # Try to find sqlite3 in PATH
    try {
        $sqlite3Exe = Get-Command sqlite3 -ErrorAction Stop | Select-Object -ExpandProperty Source
    } catch {
        Write-Host "Error: sqlite3 command not found in PATH. Please install SQLite or specify path with -Sqlite3Path parameter." -ForegroundColor Red
        Write-Host "Download from: https://www.sqlite.org/download.html" -ForegroundColor Yellow
        Write-Host "" -ForegroundColor Yellow
        Write-Host "Usage: .\vacuum_db.ps1 -Sqlite3Path 'C:\path\to\sqlite3.exe'" -ForegroundColor Yellow
        exit 1
    }
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
    & $sqlite3Exe $DB_PATH "VACUUM;"
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
