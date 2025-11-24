#!/bin/bash
# Quick fix script for 203/EXEC error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Fixing 203/EXEC error..."
echo ""

# 1. Make sure scripts are executable
echo "1. Making scripts executable..."
chmod +x start-kiosk.sh
chmod +x exit-kiosk.sh
chmod +x stop-kiosk-service.sh

# 2. Verify bash exists
BASH_PATH=$(which bash)
if [ -z "$BASH_PATH" ]; then
    BASH_PATH="/bin/bash"
fi
echo "2. Bash path: $BASH_PATH"

# 3. Check if bash exists
if [ ! -f "$BASH_PATH" ]; then
    echo "❌ Error: Bash not found at $BASH_PATH"
    exit 1
fi

# 4. Update service file to use full bash path
SERVICE_FILE="/etc/systemd/system/fortune-cookie-kiosk.service"
if [ -f "$SERVICE_FILE" ]; then
    echo "3. Updating service file..."
    sudo sed -i "s|^ExecStart=.*start-kiosk.sh|ExecStart=$BASH_PATH $SCRIPT_DIR/start-kiosk.sh|" "$SERVICE_FILE"
    echo "✅ Service file updated"
else
    echo "❌ Service file not found. Run ./setup-kiosk.sh first"
    exit 1
fi

# 5. Verify script is executable
if [ ! -x "$SCRIPT_DIR/start-kiosk.sh" ]; then
    echo "❌ Error: start-kiosk.sh is still not executable"
    exit 1
fi

# 6. Reload systemd
echo "4. Reloading systemd..."
sudo systemctl daemon-reload

echo ""
echo "✅ Fix complete!"
echo ""
echo "Try starting the service:"
echo "  sudo systemctl start fortune-cookie-kiosk.service"
echo ""
echo "Check status:"
echo "  sudo systemctl status fortune-cookie-kiosk.service"

