# Rebuild and Restart Docker Containers
# This script stops containers, rebuilds images with no cache, and restarts everything

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Rebuilding and Restarting Docker Services" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is available
$dockerCommand = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCommand) {
    Write-Host "Error: Docker command not found" -ForegroundColor Red
    Write-Host "Please install Docker Desktop for Windows" -ForegroundColor Red
    exit 1
}

# Determine which command to use
$composeV1 = Get-Command docker-compose -ErrorAction SilentlyContinue
if ($composeV1) {
    $dockerCmd = "docker-compose"
} else {
    $dockerCmd = "docker compose"
}

Write-Host "Step 1: Stopping all running containers..." -ForegroundColor Yellow
& $dockerCmd.Split() down

Write-Host ""
Write-Host "Step 2: Removing old images (optional cleanup)..." -ForegroundColor Yellow
$response = Read-Host "Do you want to remove old images? This will free up disk space. (y/N)"
if ($response -eq "y" -or $response -eq "Y") {
    & $dockerCmd.Split() down --rmi local
    Write-Host "Old images removed" -ForegroundColor Green
} else {
    Write-Host "Skipping image removal" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Step 3: Rebuilding images with no cache..." -ForegroundColor Yellow
& $dockerCmd.Split() build --no-cache

Write-Host ""
Write-Host "Step 4: Starting all services..." -ForegroundColor Yellow
& $dockerCmd.Split() up -d

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Rebuild and restart complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services are now running. Check status with:" -ForegroundColor Cyan
Write-Host "  $dockerCmd ps" -ForegroundColor White
Write-Host ""
Write-Host "View logs with:" -ForegroundColor Cyan
Write-Host "  $dockerCmd logs -f" -ForegroundColor White
Write-Host ""
