#!/bin/bash
# Setup system-level keyboard shortcut to exit kiosk mode
# This uses xbindkeys to create a global keyboard shortcut

set -e

echo "Setting up keyboard shortcut to exit kiosk mode..."
echo ""

# Check if xbindkeys is installed
if ! command -v xbindkeys &> /dev/null; then
    echo "Installing xbindkeys..."
    sudo apt-get update
    sudo apt-get install -y xbindkeys
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create xbindkeys configuration
XBINDKEYS_CONFIG="$HOME/.xbindkeysrc"

# Check if configuration already exists
if [ -f "$XBINDKEYS_CONFIG" ]; then
    # Check if our shortcut is already configured
    if grep -q "fortune-cookie-kiosk" "$XBINDKEYS_CONFIG"; then
        echo "Keyboard shortcut already configured in $XBINDKEYS_CONFIG"
        exit 0
    fi
    # Backup existing config
    cp "$XBINDKEYS_CONFIG" "$XBINDKEYS_CONFIG.backup"
    echo "" >> "$XBINDKEYS_CONFIG"
    echo "# Fortune Cookie Kiosk Exit Shortcut" >> "$XBINDKEYS_CONFIG"
else
    echo "# Fortune Cookie Kiosk Exit Shortcut" > "$XBINDKEYS_CONFIG"
fi

# Add keyboard shortcut configuration
# Ctrl+Shift+E to exit kiosk mode
cat >> "$XBINDKEYS_CONFIG" << 'EOF'
# Exit Fortune Cookie kiosk mode (Ctrl+Shift+E)
"sudo systemctl stop fortune-cookie-kiosk.service"
  control+shift + e
EOF

echo "Keyboard shortcut configured: Ctrl+Shift+E"
echo ""
echo "Configuration saved to: $XBINDKEYS_CONFIG"
echo ""

# Kill existing xbindkeys if running
killall xbindkeys 2>/dev/null || true

# Start xbindkeys
echo "Starting xbindkeys..."
xbindkeys

# Check if xbindkeys started successfully
sleep 1
if pgrep -x "xbindkeys" > /dev/null; then
    echo "✅ xbindkeys started successfully!"
    echo ""
    echo "Keyboard shortcut active: Press Ctrl+Shift+E to exit kiosk mode"
else
    echo "⚠️  Warning: xbindkeys may not have started properly"
    echo "You may need to start it manually: xbindkeys"
fi

echo ""
echo "To make xbindkeys start automatically on login, add this to ~/.xprofile:"
echo "  xbindkeys &"
echo ""

