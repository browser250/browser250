#!/bin/bash
# macOS Double-Click Installation Router for Browser 250

# Map the exact directory path where this specific file sits on the system
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "          LAUNCHING BROWSER 250 INSTALLATION SYSTEM       "
echo "=========================================================="

# Forward execution directly into our core installation script layer
./install_mac.sh

echo ""
echo "Press any key to close this setup window..."
read -n 1 -s
