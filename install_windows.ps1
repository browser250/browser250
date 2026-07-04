# Browser 250 Windows WSL2/Docker Deployment Script
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

Write-Host "Initializing Browser 250 Windows Environment..." -ForegroundColor Cyan

# Create localized storage directory
if (-not (Test-Path ".\win_config")) {
    New-Item -ItemType Directory -Path ".\win_config" | Out-Null
}

# Stop any conflicting active containers
Write-Host "Stopping existing instances..." -ForegroundColor Yellow
docker compose -f docker-compose-windows.yml down --volumes --remove-orphans 2>$null

# Build and execute the Windows container framework
Write-Host "Compiling and launching container layers..." -ForegroundColor Green
docker compose -f docker-compose-windows.yml up -d --build

# Verify runtime status
Write-Host "Verifying execution state..." -ForegroundColor Cyan
docker ps --filter name=clean_browser

Write-Host "Deployment Complete. Use Docker Desktop to manage the runtime lifecycle." -ForegroundColor Green
