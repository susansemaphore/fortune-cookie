# Kiosk Mode Quick Reference

## Initial Setup (One Time)

```bash
cd fortune-teller
./setup-kiosk.sh
```

This will:
- Install required packages
- Configure system settings
- Set up auto-start service
- Optionally enable and start the kiosk

## Daily Operations

### Start Kiosk
```bash
sudo systemctl start fortune-cookie-kiosk.service
```

### Stop Kiosk
```bash
sudo systemctl stop fortune-cookie-kiosk.service
# OR
./exit-kiosk.sh
```

### Check Status
```bash
sudo systemctl status fortune-cookie-kiosk.service
```

### View Logs
```bash
journalctl -u fortune-cookie-kiosk.service -f
```

### Enable/Disable Auto-Start
```bash
# Enable (starts on boot)
sudo systemctl enable fortune-cookie-kiosk.service

# Disable (won't start on boot)
sudo systemctl disable fortune-cookie-kiosk.service
```

## Manual Testing (Without Service)

```bash
./start-kiosk.sh
```

Press `Ctrl+C` to stop.

## Exiting Kiosk Mode

### Keyboard Shortcut (Easiest)
Press **Ctrl+Shift+E** anywhere in the kiosk to exit. A confirmation dialog will appear.

### Other Methods

1. **SSH into Pi**: `ssh pi@raspberrypi` then `sudo systemctl stop fortune-cookie-kiosk.service`
2. **Switch TTY**: Press `Ctrl+Alt+F1`, login, then stop service
3. **Terminal**: Run `./exit-kiosk.sh` if you have terminal access

## Files Created

- `start-kiosk.sh` - Main startup script (hides cursor, starts Flask, launches browser)
- `setup-kiosk.sh` - One-time setup script
- `exit-kiosk.sh` - Stop kiosk mode script
- `stop-kiosk-service.sh` - Helper script for stopping service (used by keyboard shortcut)
- `setup-keyboard-shortcut.sh` - Optional: Setup keyboard shortcut separately
- `fortune-cookie-kiosk.service` - Systemd service file

## What Kiosk Mode Does

✅ Full-screen browser (no UI elements)  
✅ Hidden mouse cursor  
✅ No screen blanking  
✅ Auto-start on boot  
✅ Auto-restart on crash  
✅ Touch-optimized interface  

