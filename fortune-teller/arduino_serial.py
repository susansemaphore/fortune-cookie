"""
Arduino serial communication module.
Handles sending data to Arduino via USB/UART.
"""
import serial
import serial.tools.list_ports
import json
import time
from arduino_data import format_for_arduino_json


class ArduinoSerial:
    """Manages serial connection to Arduino."""
    
    def __init__(self, port=None, baudrate=9600, timeout=1):
        """
        Initialize Arduino serial connection.
        
        Args:
            port (str): Serial port path (e.g., '/dev/ttyUSB0' or 'COM3')
                       If None, will attempt to auto-detect Arduino
            baudrate (int): Baud rate (must match Arduino sketch)
            timeout (int): Read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self.is_connected = False
        
    def connect(self):
        """Establish connection to Arduino."""
        try:
            if not self.port:
                print("\n" + "="*70)
                print("🔍 AUTO-DETECTING ARDUINO...")
                print("="*70)
                self.port = self.find_arduino_port()
                if not self.port:
                    print("⚠️  No Arduino found. Data will be printed to console only.")
                    print("="*70 + "\n")
                    return False
            
            print(f"\n🔌 Attempting to connect to: {self.port}")
            print(f"   Baud rate: {self.baudrate}")
            
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            
            # Wait for Arduino to reset after serial connection
            print("   Waiting for Arduino to initialize...")
            time.sleep(2)
            
            self.is_connected = True
            print(f"✅ CONNECTED to Arduino on {self.port}")
            print("="*70 + "\n")
            return True
            
        except serial.SerialException as e:
            print(f"❌ Failed to connect to Arduino on {self.port}: {e}")
            print("="*70 + "\n")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Close serial connection."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.is_connected = False
            print("🔌 Disconnected from Arduino")
    
    def send_json(self, data_dict):
        """
        Send JSON data to Arduino.
        
        Args:
            data_dict (dict): Data to send
            
        Returns:
            bool: True if sent successfully
        """
        try:
            json_string = json.dumps(data_dict, separators=(',', ':'))
            return self.send_data(json_string)
        except Exception as e:
            print(f"❌ Error preparing JSON: {e}")
            return False
    
    def send_data(self, data_string):
        """
        Send string data to Arduino.
        Adds tilde (~) terminator for Arduino's Serial.readStringUntil().
        Using ~ instead of newline since fortunes may contain \n characters.
        
        Args:
            data_string (str): String to send
            
        Returns:
            bool: True if sent successfully
        """
        if not self.is_connected:
            print("⚠️  Not connected to Arduino. Data:")
            print(f"   {data_string}")
            return False
        
        try:
            # Add tilde terminator for Arduino parsing (~ won't appear in fortunes)
            message = data_string + '~'
            self.serial_connection.write(message.encode('utf-8'))
            self.serial_connection.flush()
            
            print(f"📤 Sent to Arduino: {data_string}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending to Arduino: {e}")
            return False
    
    def read_response(self, timeout=2):
        """
        Read response from Arduino.
        
        Args:
            timeout (int): How long to wait for response
            
        Returns:
            str: Response from Arduino, or None if timeout
        """
        if not self.is_connected:
            return None
        
        try:
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode('utf-8').strip()
                print(f"📥 Arduino response: {response}")
                return response
        except Exception as e:
            print(f"❌ Error reading from Arduino: {e}")
            return None
    
    @staticmethod
    def find_arduino_port():
        """
        Auto-detect Arduino port.
        
        Returns:
            str: Port path if found, None otherwise
        """
        ports = serial.tools.list_ports.comports()
        
        if not ports:
            print("   ❌ No serial devices found")
            return None
        
        print(f"\n   Found {len(ports)} serial device(s):")
        
        for i, port in enumerate(ports, 1):
            print(f"\n   [{i}] {port.device}")
            print(f"       Description: {port.description}")
            print(f"       Hardware ID: {port.hwid}")
            if port.manufacturer:
                print(f"       Manufacturer: {port.manufacturer}")
            
            # Common Arduino identifiers
            arduino_keywords = [
                'Arduino', 'CH340', 'CH341', 'CP2102', 'CP210x', 'FTDI', 'FT232',
                'USB Serial', 'ttyUSB', 'ttyACM', 'cu.usb', 'usbserial', 'usbmodem'
            ]
            
            # Check if port description matches Arduino patterns
            for keyword in arduino_keywords:
                if keyword.lower() in port.description.lower() or \
                   keyword.lower() in port.device.lower() or \
                   (port.manufacturer and keyword.lower() in port.manufacturer.lower()):
                    print(f"       ✅ ARDUINO DETECTED!")
                    print(f"\n   🎯 Selected Arduino port: {port.device}")
                    return port.device
        
        print("\n   ❌ No Arduino detected automatically")
        print("   💡 If your Arduino is listed above, specify it manually in app.py")
        return None
    
    @staticmethod
    def list_available_ports():
        """
        List all available serial ports.
        Useful for manual port selection.
        
        Returns:
            list: List of available port paths
        """
        ports = serial.tools.list_ports.comports()
        port_list = []
        
        print("\n📋 Available Serial Ports:")
        for port in ports:
            port_list.append(port.device)
            print(f"   {port.device}")
            print(f"      Description: {port.description}")
            print(f"      Hardware ID: {port.hwid}")
        
        return port_list


# Global Arduino connection instance
arduino = None


def init_arduino(port=None, baudrate=9600):
    """
    Initialize global Arduino connection.
    
    Args:
        port (str): Serial port path (None for auto-detect)
        baudrate (int): Baud rate (must match Arduino sketch)
    
    Returns:
        ArduinoSerial: Arduino connection object
    """
    global arduino
    arduino = ArduinoSerial(port=port, baudrate=baudrate)
    arduino.connect()
    return arduino


def get_arduino():
    """Get the global Arduino connection instance."""
    global arduino
    return arduino

