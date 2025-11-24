#!/bin/bash
# Exit kiosk mode script
# This script stops the kiosk service and restores normal desktop

echo "Stopping Fortune Cookie kiosk service..."
sudo systemctl stop fortune-cookie-kiosk.service

echo "Killing any remaining Chromium processes..."
killall chromium-browser 2>/dev/null || true
killall unclutter 2>/dev/null || true

echo "Kiosk mode stopped. Desktop should be restored."
echo ""
echo "To restart kiosk mode:"
echo "  sudo systemctl start fortune-cookie-kiosk.service"
echo ""
echo "To disable auto-start:"
echo "  sudo systemctl disable fortune-cookie-kiosk.service"

