#!/bin/bash
# Native Hardware Accelerated Entrypoint for Browser 250

set -e

echo "Launching Browser 250 Core on Host Display Channel..."
exec python3 /app/clean_browser.py
