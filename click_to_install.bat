@echo off
cd /d "%~dp0"

:: Enforce Administrative Privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process '%~f0' -ArgumentList '%1' -Verb RunAs"
    exit
)

if "%1"=="run" goto launch

echo ====================================================
echo   Validating Docker Engine Environment...
echo ====================================================
echo.

where docker >nul 2>&1
if %errorlevel% neq 0 (
    if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" goto start_docker
    echo [NOTICE] Docker Desktop was not found on this system.
    echo Downloading and deploying Docker Desktop cleanly via Winget...
    winget install --id Docker.DockerDesktop --silent --accept-source-agreements --accept-package-agreements
    echo.
    echo Installation triggered. Please run this batch file again once installation finishes.
    pause
    exit
)

:check_running
docker info >nul 2>&1
if %errorlevel% eq 0 goto docker_ready

:start_docker
echo Docker Engine is offline. Initializing Docker Desktop Subsystems...
if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" (
    start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
) else (
    echo [ERROR] Cannot locate Docker Desktop executable path. Launch it manually.
    pause
    exit
)

set count=0
:install_loop
timeout /t 5 /nobreak >nul
docker info >nul 2>&1
if %errorlevel% eq 0 goto docker_ready
set /a count+=1
echo Waiting for Docker Daemon to turn green... (%count%/30)
if %count% gtr 30 goto docker_timeout
goto install_loop

:docker_ready
echo Docker Daemon is verified active and running. Proceeding to deploy application...
echo.

docker compose -f docker-compose-windows.yml down --volumes --remove-orphans 2>nul
docker compose -f docker-compose-windows.yml up -d --build

echo.
echo Generating Native Windows Desktop Shortcut...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Browser 250.lnk')); $s.TargetPath = '%~f0'; $s.Arguments = 'run'; $s.IconLocation = 'shell32.dll,220'; $s.Save()"

echo.
echo ====================================================
echo   Setup Complete! Use the 'Browser 250' Desktop Icon.
echo ====================================================
pause
exit

:docker_timeout
echo [ERROR] Docker Engine timed out during initialization. Open Docker Desktop manually.
pause
exit

:launch
set count=0
:launch_check
docker info >nul 2>&1
if %errorlevel% eq 0 goto launch_container

if %count% eq 0 (
    echo Docker is closed. Waking up Docker Engine before drawing desktop window...
    if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" (
        start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
    )
)

timeout /t 5 /nobreak >nul
set /a count+=1
echo Waiting for Engine synchronization... (%count%/30)
if %count% gtr 30 goto docker_timeout
goto launch_check

:launch_container
echo Cycling Browser 250 Desktop Window...
docker compose -f docker-compose-windows.yml down 2>nul
docker compose -f docker-compose-windows.yml up -d

timeout /t 3 /nobreak >nul
docker ps --filter "name=clean_browser" --filter "status=running" | findstr "clean_browser" >nul
if %errorlevel% neq 0 (
    echo.
    echo ====================================================
    echo   [CRITICAL ERROR] Browser container crashed on boot!
    echo   Dumping container error logs below:
    echo ====================================================
    echo.
    docker logs clean_browser
    echo.
    echo ====================================================
    pause
)
exit
