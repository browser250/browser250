#!/bin/bash
# Linux Automated Lifecycle Installer for Browser 250
# Target: Ubuntu, Debian, Mint (GNOME/XFCE/KDE Desktop Environments)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_PATH="$HOME/Desktop"
LAUNCHER_FILE="$HOME/.local/share/applications/browser250.desktop"
DESKTOP_LAUNCHER="$DESKTOP_PATH/browser250.desktop"

echo "=========================================================="
echo "          INITIALIZING BROWSER 250 LINUX INSTALLER        "
echo "=========================================================="

# 1. Verify and Install Docker Engine Dependencies via Native APT
if ! command -v docker &> /dev/null; then
    echo "[PREREQUISITE] Docker Engine missing. Injecting repository layout and installing..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose-v2
    
    # Enable and start the system container daemon automatically
    sudo systemctl enable --now docker
    
    # Bind current user to docker group to bypass sudo execution locks
    sudo usermod -aG docker "$USER"
    echo "[SUCCESS] Docker Engine successfully deployed. Please log out of your Linux session, log back in to refresh group permissions, and re-run this script to complete installation."
    exit 0
else
    echo "[OK] Docker Engine presence verified on Linux system."
fi

# 2. Compile and Spin Up VNC/noVNC Container Stacks
echo "Building Docker container layers and locking internal display targets..."
cd "$PROJECT_DIR"
docker compose up -d --build

# 3. Compile Native Linux Desktop Entry Shortcuts
echo "Generating system menu launcher configurations..."
mkdir -p "$HOME/.local/share/applications"

cat << EOF > "$LAUNCHER_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=Browser 250
Comment=Launch Browser 250 Sovereign Container Window
Exec=bash -c "cd $PROJECT_DIR && docker compose up -d && xdg-open http://localhost:8080/vnc.html"
Icon=security-high
Terminal=false
Categories=Network;WebBrowser;
EOF

# Clone the launcher straight to the visible user Desktop path
cp "$LAUNCHER_FILE" "$DESKTOP_LAUNCHER"

# Set structural execution bits so the desktop context manager recognizes the launcher
chmod +x "$LAUNCHER_FILE"
chmod +x "$DESKTOP_LAUNCHER"

# Trust the desktop launcher if running under a GNOME system environment
gio set "$DESKTOP_LAUNCHER" metadata::trusted true 2>/dev/null || true

echo "=========================================================="
echo " LINUX INSTALLATION RUN COMPLETE!"
echo " Click the 'Browser 250' icon added to your Desktop or app list to launch."
echo "=========================================================="
