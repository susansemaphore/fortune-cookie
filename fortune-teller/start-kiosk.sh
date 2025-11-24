#!/bin/bash
# Fortune Cookie Kiosk Mode Startup Script
# This script starts the Flask app and launches Chromium in full kiosk mode

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Hide the mouse cursor (unclutter)
# If unclutter is not installed, install it first: sudo apt-get install unclutter
unclutter -idle 0 -root &

# Disable screen blanking and power management
xset s off
xset -dpms
xset s noblank

# Wait a moment for Flask to be ready
sleep 2

# Start Flask app in background (production mode, no debug)
source venv/bin/activate
# Set FLASK_DEBUG=false for production kiosk mode
FLASK_DEBUG=false python app.py &
FLASK_PID=$!

# Wait for Flask to start (check if port 5001 is listening)
echo "Waiting for Flask app to start..."
for i in {1..30}; do
    if nc -z localhost 5001 2>/dev/null; then
        echo "Flask app is ready!"
        break
    fi
    sleep 1
done

# Launch Chromium in full kiosk mode
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

