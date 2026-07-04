@echo off
:: Browser 250 - Automated Windows Double-Click Launcher
cd /d "%~dp0"

echo ====================================================
echo   Launching Browser 250 Windows Deployment Layer...
echo ====================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File ".\install_windows.ps1"

echo.
echo ====================================================
echo   Execution complete. You can now close this window.
echo ====================================================
pause
