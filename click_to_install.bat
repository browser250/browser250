@echo off
:: Windows Double-Click Launcher for Browser 250
:: Forces administrative elevation and bypasses execution policies automatically

:: Check for administrative rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrative privileges verified. Launching installation engine...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_windows.ps1"
) else (
    echo Requesting Administrator Elevation...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
pause
