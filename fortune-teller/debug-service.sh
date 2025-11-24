#!/bin/bash
# Debug script to check service status and logs

echo "=========================================="
echo "Fortune Cookie Kiosk Service Debug"
echo "=========================================="
echo ""

echo "1. Service Status:"
sudo systemctl status fortune-cookie-kiosk.service --no-pager -l
echo ""

echo "2. Recent Service Logs (last 50 lines):"
journalctl -u fortune-cookie-kiosk.service -n 50 --no-pager
echo ""

echo "3. Startup Script Log:"
if [ -f /tmp/fortune-cookie-kiosk.log ]; then
    echo "Last 50 lines of startup log:"
    tail -n 50 /tmp/fortune-cookie-kiosk.log
else
    echo "No startup log found at /tmp/fortune-cookie-kiosk.log"
fi
echo ""

echo "4. Checking processes:"
echo "Flask processes:"
ps aux | grep "[p]ython.*app.py" || echo "No Flask process found"
echo ""
echo "Chromium processes:"
ps aux | grep "[c]hromium-browser" || echo "No Chromium process found"
echo ""

echo "5. Checking port 5001:"
if nc -z localhost 5001 2>/dev/null; then
    echo "Port 5001 is listening"
else
    echo "Port 5001 is NOT listening"
fi
echo ""

echo "6. Checking X server:"
if xset q &>/dev/null; then
    echo "X server is accessible"
    echo "DISPLAY: $DISPLAY"
else
    echo "X server is NOT accessible"
    echo "DISPLAY: ${DISPLAY:-not set}"
fi
echo ""

echo "7. Checking virtual environment:"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    echo "Virtual environment found at: $SCRIPT_DIR/venv"
else
    echo "Virtual environment NOT found at: $SCRIPT_DIR/venv"
fi
echo ""

echo "8. Checking service file:"
if [ -f /etc/systemd/system/fortune-cookie-kiosk.service ]; then
    echo "Service file exists:"
    cat /etc/systemd/system/fortune-cookie-kiosk.service
else
    echo "Service file NOT found at /etc/systemd/system/fortune-cookie-kiosk.service"
fi
echo ""

echo "=========================================="
echo "Debug complete"
echo "=========================================="

