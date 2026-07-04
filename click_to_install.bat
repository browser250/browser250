@echo off
cd /d "%~dp0"

:: Enforce Administrative Privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges to manage Docker subsystems...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process '%~f0' -ArgumentList '%1' -Verb RunAs"
    exit /b
)

if "%1"=="run" goto launch

echo ====================================================
echo   Validating Docker Engine Environment...
echo ====================================================
echo.

:: Check if Docker CLI is installed
where docker >nul 2>&1
if %errorlevel% neq 0 (
    if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" goto start_docker
    
    echo [NOTICE] Docker Desktop was not found on this system.
    echo Downloading and deploying Docker Desktop cleanly via Winget...
    echo Please wait, this process takes a few minutes...
    echo.
    
    winget install --id Docker.DockerDesktop --silent --accept-source-agreements --accept-package-agreements
    if %errorlevel% neq 0 (
        echo [CRITICAL ERROR] Automated installation failed. Please install Docker Desktop manually.
        pause
        exit /b
    )
    echo Installation complete. Refreshing environment variables...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
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
    exit /b
)

echo Waiting for Docker Daemon virtualization layer to turn green...
set count=0
:loop
timeout /t 5 /nobreak >nul
docker info >nul 2>&1
if %errorlevel% neq 0 (
    set /a count+=1
    if %count% geq 36 (
        echo [ERROR] Docker Engine timed out during initialization. Check WSL2 status.
        pause
        exit /b
    )
    goto loop
)

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

:launch
:: Ensure engine is alive when desktop shortcut is triggered
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is closed. Waking up Docker Engine before drawing desktop window...
    if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" (
        start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
    )
    set count=0
    :launch_loop
    timeout /t 5 /nobreak >nul
    docker info >nul 2>&1
    if %errorlevel% neq 0 (
        set /a count+=1
        if %count% geq 36 (
            echo [ERROR] Failed to wake up Docker Engine.
            pause
            exit
        )
        goto launch_loop
    )
)

echo Cycling Browser 250 Desktop Window...
docker compose -f docker-compose-windows.yml down 2>nul
docker compose -f docker-compose-windows.yml up -d
exit
