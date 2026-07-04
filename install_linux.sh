#!/bin/bash
# Native Linux Installer for Browser 250

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_PATH="$HOME/Desktop"
LAUNCHER_FILE="$HOME/.local/share/applications/browser250.desktop"
DESKTOP_LAUNCHER="$DESKTOP_PATH/browser250.desktop"

echo "=========================================================="
echo "      INITIALIZING BROWSER 250 RUNTIME ENVIRONMENT        "
echo "=========================================================="

sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2 x11-xserver-utils

xhost +local:docker

echo "Building core container layers..."
cd "$PROJECT_DIR"
docker compose down --volumes --remove-orphans 2>/dev/null || true
docker compose up -d --build

echo "Generating native system desktop application shortcuts..."
mkdir -p "$HOME/.local/share/applications"

cat << EOF > "$LAUNCHER_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=Browser 250
Comment=Open Browser 250 Native Application Window
Exec=bash -c "xhost +local:docker && cd $PROJECT_DIR && DISPLAY=$DISPLAY XAUTHORITY=$HOME/.Xauthority docker compose up -d"
Icon=security-high
Terminal=false
Categories=Network;WebBrowser;
EOF

cp "$LAUNCHER_FILE" "$DESKTOP_LAUNCHER"
chmod +x "$LAUNCHER_FILE"
chmod +x "$DESKTOP_LAUNCHER"

gio set "$DESKTOP_LAUNCHER" metadata::trusted true 2>/dev/null || true

echo "=========================================================="
echo " NATIVE INSTALLATION COMPLETE!"
echo "=========================================================="
