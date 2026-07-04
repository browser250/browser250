@echo off
cd /d "%~dp0"

if "%1"=="run" goto launch

echo ====================================================
echo   Installing Browser 250 for Windows (WSLg Mode)...
echo ====================================================
echo.

:: Execute via the WSL layer to bind display sockets natively
wsl docker compose -f docker-compose-windows.yml down --volumes --remove-orphans 2>nul
wsl docker compose -f docker-compose-windows.yml up -d --build

echo.
echo Generating Native Windows Desktop Shortcut...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Browser 250.lnk')); $s.TargetPath = '%~f0'; $s.Arguments = 'run'; $s.IconLocation = 'shell32.dll,220'; $s.Save()"

echo.
echo ====================================================
echo   Setup Complete! Use the 'Browser 250' Desktop Icon.
echo ====================================================
pause
exit

:launch
echo Cycling Browser 250 Desktop Window...
wsl docker compose -f docker-compose-windows.yml down 2>nul
wsl docker compose -f docker-compose-windows.yml up -d

echo Diagnostics: Verifying container runtime stability...
timeout /t 3 /nobreak >nul

wsl docker ps --filter "name=clean_browser" --filter "status=running" | findstr "clean_browser" >nul
if %errorlevel% neq 0 (
    echo.
    echo ====================================================
    echo   [CRITICAL ERROR] Browser container crashed on boot!
    echo   Dumping container error logs below:
    echo ====================================================
    echo.
    wsl docker logs clean_browser
    echo.
    echo ====================================================
    pause
)
exit
