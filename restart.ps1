# Quick Restart Docker Containers
# This script simply restarts all containers without rebuilding

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Restarting Docker Services" -ForegroundColor Cyan
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

Write-Host "Restarting all containers..." -ForegroundColor Yellow
& $dockerCmd.Split() restart

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Restart complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services are now running. Check status with:" -ForegroundColor Cyan
Write-Host "  $dockerCmd ps" -ForegroundColor White
Write-Host ""
Write-Host "View logs with:" -ForegroundColor Cyan
Write-Host "  $dockerCmd logs -f" -ForegroundColor White
Write-Host ""
