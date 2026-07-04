# Windows 10 / 11 Automated Lifecycle Installer for Browser 250
# Force administrative elevation rules
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

# Explicitly grab the absolute path string of the folder where this script is running
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Browser 250.lnk"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         INITIALIZING BROWSER 250 WINDOWS INSTALLER       "
Write-Host "==========================================================" -ForegroundColor Cyan

# Check for Docker installation on host machine
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[PREREQUISITE] Docker Engine missing. Deploying Docker Desktop via WinGet..." -ForegroundColor Yellow
    winget install --id Docker.DockerDesktop --silent --accept-package-agreements --accept-source-agreements
    Write-Host "[SUCCESS] Docker Desktop deployed. Please launch Docker Desktop from your start menu, ensure the backend engine initializes, and rerun this installer script to complete your desktop configuration." -ForegroundColor Cyan
    Exit
} else {
    Write-Host "[OK] Docker Engine presence verified on host machine." -ForegroundColor Green
}

# Change directory to where the project files actually live before running compose
Set-Location -Path $ScriptDir

# Spin up cross-platform container stack via compose configuration
Write-Host "Compiling container images and mapping layout tables..." -ForegroundColor Cyan
docker compose up -d --build

# Generate native Windows Desktop Shortcut matrix
Write-Host "Planting native launch icon on desktop workspace..." -ForegroundColor Cyan
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c cd /d `"$ScriptDir`" && docker compose up -d && start http://localhost:8080/vnc.html"
$Shortcut.Description = "Launch Browser 250 Container Architecture"
$Shortcut.WorkingDirectory = "$ScriptDir"
$Shortcut.IconLocation = "shell32.dll, 44"
$Shortcut.Save()

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " WINDOWS INSTALLATION COMPLETE!"
Write-Host " Double-click the 'Browser 250' launch icon on your Desktop anytime to deploy."
Write-Host "==========================================================" -ForegroundColor Green
