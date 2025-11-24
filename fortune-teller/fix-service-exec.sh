#!/bin/bash
# Quick fix script for 203/EXEC and 200/CHDIR errors

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Fixing service errors (203/EXEC, 200/CHDIR)..."
echo ""

# 1. Verify directory exists
echo "1. Checking working directory..."
if [ ! -d "$SCRIPT_DIR" ]; then
    echo "❌ Error: Directory does not exist: $SCRIPT_DIR"
    exit 1
fi
echo "✅ Directory exists: $SCRIPT_DIR"

# 2. Make sure scripts are executable
echo "2. Making scripts executable..."
chmod +x start-kiosk.sh
chmod +x exit-kiosk.sh
chmod +x stop-kiosk-service.sh

# 3. Verify bash exists
BASH_PATH=$(which bash)
if [ -z "$BASH_PATH" ]; then
    BASH_PATH="/bin/bash"
fi
echo "3. Bash path: $BASH_PATH"

# 4. Check if bash exists
if [ ! -f "$BASH_PATH" ]; then
    echo "❌ Error: Bash not found at $BASH_PATH"
    exit 1
fi

# 5. Get current user
CURRENT_USER=$(whoami)
echo "4. Current user: $CURRENT_USER"

# 6. Update service file
SERVICE_FILE="/etc/systemd/system/fortune-cookie-kiosk.service"
if [ -f "$SERVICE_FILE" ]; then
    echo "5. Updating service file..."
    
    # Create a temporary service file with correct paths
    TMP_SERVICE=$(mktemp)
    cat > "$TMP_SERVICE" << EOF
[Unit]
Description=Fortune Cookie Kiosk Application
After=network.target graphical.target
Wants=graphical.target

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_USER
Environment=DISPLAY=:0
Environment=XAUTHORITY=$HOME/.Xauthority
Environment=HOME=$HOME
WorkingDirectory=$SCRIPT_DIR
ExecStart=$BASH_PATH $SCRIPT_DIR/start-kiosk.sh
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
TimeoutStartSec=60

[Install]
WantedBy=graphical.target
EOF
    
    # Copy to systemd directory
    sudo cp "$TMP_SERVICE" "$SERVICE_FILE"
    rm "$TMP_SERVICE"
    
    echo "✅ Service file updated with:"
    echo "   WorkingDirectory: $SCRIPT_DIR"
    echo "   ExecStart: $BASH_PATH $SCRIPT_DIR/start-kiosk.sh"
    echo "   User: $CURRENT_USER"
else
    echo "❌ Service file not found. Run ./setup-kiosk.sh first"
    exit 1
fi

# 7. Verify script is executable
if [ ! -x "$SCRIPT_DIR/start-kiosk.sh" ]; then
    echo "❌ Error: start-kiosk.sh is still not executable"
    exit 1
fi

# 8. Verify directory permissions
if [ ! -r "$SCRIPT_DIR" ]; then
    echo "⚠️  Warning: Directory may not be readable by user $CURRENT_USER"
fi

# 9. Reload systemd
echo "6. Reloading systemd..."
sudo systemctl daemon-reload

echo ""
echo "✅ Fix complete!"
echo ""
echo "Service file contents:"
sudo cat "$SERVICE_FILE"
echo ""
echo "Try starting the service:"
echo "  sudo systemctl start fortune-cookie-kiosk.service"
echo ""
echo "Check status:"
echo "  sudo systemctl status fortune-cookie-kiosk.service"

