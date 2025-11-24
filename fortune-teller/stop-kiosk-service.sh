#!/bin/bash
# Helper script to stop the kiosk service
# This can be called by xbindkeys or the Flask API

sudo systemctl stop fortune-cookie-kiosk.service

