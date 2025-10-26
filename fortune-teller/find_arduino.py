#!/usr/bin/env python3
"""
Utility script to find and list all serial ports.
Run this to identify which port your Arduino is on.

Usage:
    python find_arduino.py
"""
import serial.tools.list_ports


def main():
    """List all available serial ports with details."""
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("❌ No serial ports found!")
        return
    
    print("\n" + "="*70)
    print("AVAILABLE SERIAL PORTS")
    print("="*70)
    
    arduino_ports = []
    other_ports = []
    
    for port in ports:
        # Categorize ports
        is_arduino = False
        arduino_keywords = [
            'Arduino', 'CH340', 'CH341', 'CP2102', 'FTDI', 
            'USB Serial', 'ttyUSB', 'ttyACM', 'cu.usb', 'FT232'
        ]
        
        for keyword in arduino_keywords:
            if keyword.lower() in port.description.lower() or \
               keyword.lower() in port.device.lower():
                is_arduino = True
                break
        
        if is_arduino:
            arduino_ports.append(port)
        else:
            other_ports.append(port)
    
    # Show Arduino ports first
    if arduino_ports:
        print("\n🎯 LIKELY ARDUINO DEVICES:")
        print("-" * 70)
        for port in arduino_ports:
            print(f"\n✅ {port.device}")
            print(f"   Description: {port.description}")
            print(f"   Hardware ID: {port.hwid}")
            print(f"   Manufacturer: {port.manufacturer if port.manufacturer else 'Unknown'}")
    
    # Show other devices
    if other_ports:
        print("\n\n📱 OTHER SERIAL DEVICES (keyboard, mouse, etc):")
        print("-" * 70)
        for port in other_ports:
            print(f"\n   {port.device}")
            print(f"   Description: {port.description}")
            print(f"   Hardware ID: {port.hwid}")
    
    print("\n" + "="*70)
    
    # Provide instructions
    if arduino_ports:
        recommended_port = arduino_ports[0].device
        print(f"\n💡 RECOMMENDED: Use this port in app.py:")
        print(f"   arduino_connection = init_arduino(port='{recommended_port}', baudrate=9600)")
    else:
        print("\n⚠️  No Arduino automatically detected.")
        print("   If you know which port your Arduino is on, specify it manually:")
        if other_ports:
            print(f"   Try one of these: {', '.join([p.device for p in other_ports])}")
    
    print("\n📝 TIPS:")
    print("   • Disconnect and reconnect Arduino to see which port disappears/appears")
    print("   • On macOS/Linux: Arduino usually shows as /dev/ttyUSB* or /dev/ttyACM*")
    print("   •                  Or /dev/cu.usbserial* or /dev/cu.usbmodem*")
    print("   • On Windows: Arduino shows as COM3, COM4, COM5, etc")
    print("   • Keyboard/mouse typically DON'T show up as serial ports")
    print("   • The baud rate (9600) MUST match your Arduino sketch's Serial.begin()")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

