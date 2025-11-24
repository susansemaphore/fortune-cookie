#!/bin/bash
# Setup script for Fortune Cookie Kiosk Mode on Raspberry Pi
# Run this script once to configure your Raspberry Pi for kiosk mode

set -e

echo "=========================================="
echo "Fortune Cookie Kiosk Mode Setup"
echo "=========================================="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ] || ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    echo "⚠️  Warning: This script is designed for Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📦 Installing required packages..."
sudo apt-get update
sudo apt-get install -y \
    unclutter \
    x11-xserver-utils \
    chromium-browser \
    netcat-openbsd \
    xbindkeys

echo ""
echo "🔧 Configuring system settings..."

# Disable screen blanking in X11
if [ -f ~/.xprofile ]; then
    if ! grep -q "xset s off" ~/.xprofile; then
        echo "xset s off" >> ~/.xprofile
        echo "xset -dpms" >> ~/.xprofile
        echo "xset s noblank" >> ~/.xprofile
    fi
    # Start xbindkeys for keyboard shortcuts
    if ! grep -q "xbindkeys" ~/.xprofile; then
        echo "xbindkeys &" >> ~/.xprofile
    fi
else
    echo "xset s off" > ~/.xprofile
    echo "xset -dpms" >> ~/.xprofile
    echo "xset s noblank" >> ~/.xprofile
    echo "xbindkeys &" >> ~/.xprofile
fi
chmod +x ~/.xprofile

# Make startup scripts executable
chmod +x "$SCRIPT_DIR/start-kiosk.sh"
chmod +x "$SCRIPT_DIR/exit-kiosk.sh"
chmod +x "$SCRIPT_DIR/stop-kiosk-service.sh"

echo ""
echo "📝 Setting up systemd service..."

# Get absolute path to service file
SERVICE_FILE="$SCRIPT_DIR/fortune-cookie-kiosk.service"

# Update service file with correct paths
USER_HOME=$(eval echo ~$USER)
FORTUNE_DIR="$SCRIPT_DIR"
sed -i "s|/home/pi|$USER_HOME|g" "$SERVICE_FILE"
sed -i "s|/home/pi/Documents/fortune-cookie/fortune-teller|$FORTUNE_DIR|g" "$SERVICE_FILE"
sed -i "s|User=pi|User=$USER|g" "$SERVICE_FILE"

# Copy service file to systemd directory
sudo cp "$SERVICE_FILE" /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

echo ""
echo "⌨️  Setting up keyboard shortcut (Ctrl+Shift+E to exit kiosk)..."

# Create xbindkeys configuration for keyboard shortcut
XBINDKEYS_CONFIG="$HOME/.xbindkeysrc"
EXIT_SCRIPT="$SCRIPT_DIR/exit-kiosk.sh"

# Create or update xbindkeys config
if [ -f "$XBINDKEYS_CONFIG" ]; then
    # Remove old fortune-cookie entries if they exist
    sed -i '/# Fortune Cookie Kiosk Exit Shortcut/,+2d' "$XBINDKEYS_CONFIG" 2>/dev/null || true
    echo "" >> "$XBINDKEYS_CONFIG"
else
    touch "$XBINDKEYS_CONFIG"
fi

# Add keyboard shortcut configuration
# Use exit-kiosk.sh which handles the service stop
cat >> "$XBINDKEYS_CONFIG" << EOF
# Fortune Cookie Kiosk Exit Shortcut (Ctrl+Shift+E)
"$EXIT_SCRIPT"
  control+shift + e
EOF

# Kill existing xbindkeys if running
killall xbindkeys 2>/dev/null || true

# Start xbindkeys
xbindkeys 2>/dev/null || echo "⚠️  Note: xbindkeys will start on next login"

echo "✅ Keyboard shortcut configured: Ctrl+Shift+E to exit kiosk mode"

# Configure sudo permissions for stop script (optional, for passwordless exit)
echo ""
read -p "Configure passwordless sudo for kiosk exit? (Recommended for keyboard shortcut) (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SUDOERS_ENTRY="$USER ALL=(ALL) NOPASSWD: $EXIT_SCRIPT"
    SUDOERS_FILE="/etc/sudoers.d/fortune-cookie-kiosk"
    
    # Check if entry already exists
    if sudo grep -q "fortune-cookie-kiosk" /etc/sudoers.d/fortune-cookie-kiosk 2>/dev/null; then
        echo "Sudo permissions already configured"
    else
        echo "$SUDOERS_ENTRY" | sudo tee "$SUDOERS_FILE" > /dev/null
        sudo chmod 0440 "$SUDOERS_FILE"
        echo "✅ Passwordless sudo configured for kiosk exit"
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To enable auto-start on boot, run:"
echo "  sudo systemctl enable fortune-cookie-kiosk.service"
echo ""
echo "To start the kiosk now, run:"
echo "  sudo systemctl start fortune-cookie-kiosk.service"
echo ""
echo "To check status:"
echo "  sudo systemctl status fortune-cookie-kiosk.service"
echo ""
echo "To view logs:"
echo "  journalctl -u fortune-cookie-kiosk.service -f"
echo ""
read -p "Enable auto-start on boot now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo systemctl enable fortune-cookie-kiosk.service
    echo "✅ Auto-start enabled!"
    echo ""
    read -p "Start the kiosk service now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo systemctl start fortune-cookie-kiosk.service
        echo "✅ Kiosk service started!"
        echo "The app should launch in kiosk mode shortly..."
    fi
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="

