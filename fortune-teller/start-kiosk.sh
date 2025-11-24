#!/bin/bash
# Fortune Cookie Kiosk Mode Startup Script
# This script starts the Flask app and launches Chromium in full kiosk mode

# Enable error handling
set -e

# Log file for debugging
LOG_FILE="/tmp/fortune-cookie-kiosk.log"
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$LOG_FILE" >&2)

echo "=========================================="
echo "Fortune Cookie Kiosk Startup"
echo "Date: $(date)"
echo "User: $(whoami)"
echo "DISPLAY: ${DISPLAY:-not set}"
echo "=========================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
echo "Working directory: $SCRIPT_DIR"

# Wait for X server to be ready (important for systemd)
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
    echo "Setting DISPLAY to :0"
fi

# Wait for X server
echo "Waiting for X server..."
for i in {1..30}; do
    if xset q &>/dev/null; then
        echo "X server is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: X server not available after 30 seconds"
        exit 1
    fi
    sleep 1
done

# Set XAUTHORITY if not set
if [ -z "$XAUTHORITY" ]; then
    export XAUTHORITY="$HOME/.Xauthority"
    echo "Setting XAUTHORITY to $XAUTHORITY"
fi

# Hide the mouse cursor (unclutter)
# If unclutter is not installed, install it first: sudo apt-get install unclutter
echo "Starting unclutter..."
unclutter -idle 0 -root &

# Disable screen blanking and power management
echo "Configuring display settings..."
xset s off || echo "Warning: xset s off failed"
xset -dpms || echo "Warning: xset -dpms failed"
xset s noblank || echo "Warning: xset s noblank failed"

# Wait a moment for Flask to be ready
sleep 2

# Start Flask app in background (production mode, no debug)
echo "Activating virtual environment..."
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found at venv/bin/activate"
    echo "Please create it with: python3 -m venv venv"
    exit 1
fi

source venv/bin/activate
echo "Virtual environment activated"

# Verify Python and Flask are available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found in virtual environment"
    exit 1
fi

echo "Starting Flask app..."
# Set FLASK_DEBUG=false for production kiosk mode
FLASK_DEBUG=false python app.py &
FLASK_PID=$!
echo "Flask PID: $FLASK_PID"

# Wait for Flask to start (check if port 5001 is listening)
echo "Waiting for Flask app to start..."
FLASK_READY=0
for i in {1..30}; do
    if nc -z localhost 5001 2>/dev/null; then
        echo "Flask app is ready!"
        FLASK_READY=1
        break
    fi
    # Check if Flask process is still running
    if ! kill -0 $FLASK_PID 2>/dev/null; then
        echo "ERROR: Flask process died before starting"
        exit 1
    fi
    sleep 1
done

if [ $FLASK_READY -eq 0 ]; then
    echo "ERROR: Flask app did not start within 30 seconds"
    echo "Checking Flask process..."
    if kill -0 $FLASK_PID 2>/dev/null; then
        echo "Flask process is running but port 5001 is not listening"
    else
        echo "Flask process is not running"
    fi
    exit 1
fi

# Launch Chromium in full kiosk mode
echo "Launching Chromium in kiosk mode..."
if ! command -v chromium-browser &> /dev/null; then
    echo "ERROR: chromium-browser not found"
    echo "Install it with: sudo apt-get install chromium-browser"
    exit 1
fi

# --kiosk: Full screen, no address bar
# --incognito: No browsing history/cache
# --noerrdialogs: Suppress error dialogs
# --disable-infobars: Remove info bars
# --disable-session-crashed-bubble: Don't show crash recovery
# --disable-restore-session-state: Don't restore previous session
# --autoplay-policy=no-user-gesture-required: Allow autoplay for audio
# --check-for-update-interval=31536000: Don't check for updates
chromium-browser \
    --kiosk \
    --incognito \
    --noerrdialogs \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --disable-restore-session-state \
    --autoplay-policy=no-user-gesture-required \
    --check-for-update-interval=31536000 \
    --disable-features=TranslateUI \
    --disable-ipc-flooding-protection \
    http://localhost:5001 &

CHROMIUM_PID=$!
echo "Chromium PID: $CHROMIUM_PID"
echo "Kiosk mode started successfully!"

# Function to cleanup on exit
cleanup() {
    echo "Shutting down..."
    kill $FLASK_PID 2>/dev/null
    kill $CHROMIUM_PID 2>/dev/null
    killall unclutter 2>/dev/null
    exit
}

# Trap signals to cleanup
trap cleanup SIGTERM SIGINT

# Wait for Chromium to exit
wait $CHROMIUM_PID

# Cleanup
cleanup

