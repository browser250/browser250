#!/bin/bash
# macOS Automated Lifecycle Installer for Browser 250

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_PATH="$HOME/Desktop"
LAUNCH_SHORTCUT="$DESKTOP_PATH/Browser_250.command"

echo "=========================================================="
echo "          INITIALIZING BROWSER 250 MAC OXYGEN SUITE       "
echo "=========================================================="

# Check for Docker CLI binary mapping on Mac system
if ! command -v docker &> /dev/null; then
    echo "[PREREQUISITE] Docker Engine missing. Searching for Homebrew Package Manager..."
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew core utilities to manage container provisioning..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
    fi
    echo "Deploying Docker Desktop Application via Homebrew Cask..."
    brew install --cask docker
    echo "[SUCCESS] Docker Desktop successfully transferred. Please launch Docker from your Mac Applications folder, authorize initial system rules, and rerun this script."
    exit 0
else
    echo "[OK] Docker Engine presence verified on Mac environment."
fi

# Bring up background container daemon
echo "Compiling localized container configurations..."
cd "$PROJECT_DIR" && docker compose up -d --build

# Generate executable double-clickable Apple desktop launch asset
echo "Planting native execution icon on macOS desktop workspace..."
cat << EOF > "$LAUNCH_SHORTCUT"
#!/bin/bash
cd "$PROJECT_DIR"
docker compose up -d
open "http://localhost:8080/vnc.html"
EOF

# Grant absolute execution permissions to the macOS Desktop Shortcut
chmod +x "$LAUNCH_SHORTCUT"

echo "=========================================================="
echo " MAC OS INSTALLATION RUN COMPLETE!"
echo " Double-click 'Browser_250.command' directly on your Desktop to open."
echo "=========================================================="
