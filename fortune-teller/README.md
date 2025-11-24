# 🔮 Fortune Teller (The Great Cookie)

A mystical **hardware-software hybrid interactive installation** that combines Flask web application, Arduino-controlled physical mechanisms, and a touch-screen kiosk interface to create an immersive fortune-telling experience.

## 📋 Project Description

**The Great Cookie** is an interactive art installation that guides users through a multi-step mystical journey to receive a personalized fortune. Users interact with a touch-screen kiosk to answer questions about their life (love, guidance, fortune, or surprise), then place their fingerprint on a sensor to trigger physical hardware that dispenses a printed fortune cookie.

### 🎭 What Makes This Unique

This is not just a web app—it's a **complete interactive installation**:

- ✨ **Touch-screen kiosk interface** with custom virtual keyboard
- 🎵 **Synchronized audio playback** at each step
- 🎨 **Rich visual animations** (icons, transitions, fingerprint scanning)
- 🤖 **Arduino-controlled hardware** for physical fortune dispensing
- 🔮 **Four unique paths** based on user's intent (Love, Guidance, Fortune, Surprise)
- 📡 **Real-time communication** between software and hardware via serial

### 🏗️ System Overview (Quick Reference)

```
USER (touchscreen) 
    ↓
FLASK WEB APP (Python)
    ├─ Multi-step form wizard
    ├─ Session state management  
    ├─ Audio/visual coordination
    └─ Centralized content system
    ↓
SERIAL COMMUNICATION (USB)
    ├─ Auto-detect Arduino port
    ├─ JSON data transmission
    └─ Graceful fallback if no hardware
    ↓
ARDUINO HARDWARE
    ├─ Servo motors (lid mechanism)
    ├─ Thermal printer (fortune text)
    └─ LEDs/sensors (effects)
```

### 🎯 Target Environment

- **Primary**: Raspberry Pi 4 with touchscreen in kiosk mode
- **Development**: Any computer with Python 3.7+
- **Hardware**: Arduino Uno/Mega + custom physical mechanisms
- **Display**: Full-screen kiosk mode, no keyboard/mouse needed

---

## 🎓 Complete Architecture Summary (At-a-Glance)

### Technology Stack
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5 + Jinja2 Templates | User interface |
| **Styling** | Custom CSS | Touch-optimized kiosk design |
| **JavaScript** | Vanilla JS | Virtual keyboard, audio playback |
| **Backend** | Flask (Python) | Web server, routing, sessions |
| **State** | Flask Sessions | User journey data |
| **Content** | Python dict (content.py) | Centralized text management |
| **Hardware** | Arduino (C++) | Physical mechanism control |
| **Communication** | PySerial + UART | Python ↔ Arduino data |
| **Data Format** | JSON | Structured serial transmission |
| **Media** | WAV audio, PNG/JPEG images | Multimedia experience |
| **Deployment** | Raspberry Pi + Chromium Kiosk | Production environment |

### Key Components

**1. Flask Application (`app.py`)**
- 20+ routes handling multi-step wizard
- Session management for user state
- Arduino connection initialization
- API endpoint for data inspection

**2. Serial Communication Layer (`arduino_serial.py`, `arduino_data.py`)**
- Auto-detects Arduino port on startup
- Sends user data as JSON via USB
- Gracefully handles missing hardware
- Multiple data format options

**3. Content System (`content.py`)**
- Single source of truth for all text
- Easy updates without touching HTML
- Supports conditional content

**4. Template System (`templates/`)**
- Base template with virtual keyboard
- 16 step-specific templates
- Path-specific conditional rendering
- Audio playback integration

**5. Static Assets (`static/`)**
- 100+ WAV audio files (organized by flow)
- 149+ images (animations, icons)
- Custom pixel font
- Touch-optimized CSS

### User Flow States

```
Session Data Structure:
{
  'name': str,                    # User's name
  'category': str,                # love|guidance|fortune|surprise
  '[category]_answer': str,       # Multiple choice from Step 1
  '[category]_question': str      # Free text from Step 2
}
```

### Communication Protocol

**Python → Arduino:**
```json
{
  "name": "Alice",
  "category": "love",
  "love_answer": "has_feelings",
  "love_question": "their kindness"
}
```

**Arduino → Python:**
```
ACK (acknowledgment)
```

### File Responsibilities Quick Reference

| File | What It Does | When You'd Edit It |
|------|--------------|-------------------|
| `app.py` | Routes & logic | Adding new steps/paths |
| `content.py` | All text content | Changing any displayed text |
| `arduino_serial.py` | Serial comm | Debugging Arduino connection |
| `arduino_data.py` | Data formatting | Changing data structure |
| `fortunes.py` | Fortune generation | Algorithm changes (unused currently) |
| `find_arduino.py` | Port detection | Never (utility tool) |
| `templates/*.html` | UI layout | Changing page structure |
| `static/style.css` | All styling | Visual design changes |
| `static/audio/` | Sound files | Adding/replacing audio |
| `static/images/` | Visual assets | Adding/replacing graphics |

### Critical Configuration Points

1. **`app.py` Line 14**: Flask secret key (CHANGE FOR PRODUCTION)
2. **`app.py` Line 18**: Arduino port (None = auto-detect)
3. **`app.py` Line 201**: Server host/port/debug settings
4. **Arduino sketch**: `Serial.begin(9600)` must match Python baudrate

### Typical Maintenance Tasks

| Task | Files to Edit |
|------|---------------|
| Update fortune text | `content.py` |
| Add new question | `content.py`, `templates/[category]Step*.html`, `app.py` (new route) |
| Change audio | Replace files in `static/audio/[folder]/` |
| Modify styling | `static/style.css` |
| Debug Arduino | Check `arduino_serial.py` console output, run `find_arduino.py` |
| Change Arduino behavior | Arduino `.ino` sketch (not in this repo) |

---

## 📑 Table of Contents

**Quick Start**
- [Getting Started](#-getting-started) - Setup and installation
- [Running the Application](#-running-the-application) - How to launch
- [Dependencies](#-dependencies) - Required packages

**Architecture & Documentation**
- [Module Documentation](#-module-documentation) - Detailed module breakdown
- [Project Structure](#%EF%B8%8F-project-structure) - File organization
- [System Architecture](#%EF%B8%8F-system-architecture) - Full architecture overview
- [How It Works](#-how-it-works) - User journey and data flow
- [Design Patterns Used](#-design-patterns-used) - Software patterns

**Hardware Integration**
- [Arduino Integration](#-arduino-integration) - Serial communication setup
- [Finding Arduino Port](#finding-your-arduino-port) - Auto-detection guide
- [Data Formats](#data-formats-sent-to-arduino) - JSON/CSV/Simple formats

**Deployment & Production**
- [Deployment Considerations](#-deployment-considerations) - Kiosk mode, auto-start
- [Technical Architecture Decisions](#-technical-architecture-decisions) - Why we chose each technology
- [Hardware Requirements](#hardware-requirements) - System specs

**Development & Debugging**
- [Debugging & Development Tips](#-debugging--development-tips) - Troubleshooting guide
- [Common Issues & Solutions](#-common-issues--solutions) - FAQ
- [Resources Directory](#-resources-directory) - Source materials

**Content Management**
- [Content Management](#-content-management) - How to update text
- [Troubleshooting](#-troubleshooting) - Basic issues

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Navigate to the project directory**
   ```bash
   cd /Users/susanspangenberg/Documents/fortune-teller
   ```

2. **Create a virtual environment** (if you haven't already)
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```
   
   *You should see `(venv)` appear at the beginning of your terminal prompt.*

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Running the Application

1. **Activate your virtual environment** (if not already activated)
   ```bash
   source .venv/bin/activate
   ```

2. **Run the Flask application**
   ```bash
   python app.py
   ```

3. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

4. **Stop the server**
   
   Press `Ctrl+C` in the terminal when you're done.

## 📦 Dependencies

- **Flask** (>=2.3, <4): Web framework for Python
  - Handles routing, session management, template rendering
  - Runs the web server on port 5001
- **pyserial** (3.5): Python serial port access library
  - Enables USB/UART communication with Arduino
  - Cross-platform support (Windows, macOS, Linux)

See `requirements.txt` for the complete list.

## 📚 Module Documentation

### Core Python Modules

#### `app.py` - Main Flask Application
**Purpose**: Central routing and application logic

**Key Routes**:
- `GET /` → Landing page (clears session)
- `GET /step1` → Name input
- `POST /step2` → Category selection
- `POST /step3` → Path-specific Step 1
- `POST /fingerprint-animation` → Fingerprint animation + Arduino transmission
- `GET /show-fortune` → Display final fortune
- `POST /animation/<category>` → Category transition animation
- `GET /loveStep1`, `POST /loveStep2` → Love path
- `GET /guidanceStep1`, `POST /guidanceStep2` → Guidance path
- `GET /fortuneStep1`, `POST /fortuneStep2` → Fortune path
- `GET /surpriseStep1`, `POST /surpriseStep2` → Surprise path
- `GET /api/arduino-data` → API endpoint for Arduino data in various formats

**Initialization**:
- Sets up Flask app with secret key
- Initializes Arduino connection on startup
- Auto-detects Arduino port if not specified

#### `content.py` - Content Management System
**Purpose**: Centralized text content for easy updates

**Key Constants**:
- `APP_TITLE`: Application name
- `APP_ICON`: Emoji icon
- `CONTENT`: Dictionary of all page content

**Function**:
- `get_content(page_name)`: Returns content dict for specified page

**Benefits**:
- Change text without editing HTML
- Consistent content structure
- Easy localization in future

#### `fortunes.py` - Fortune Generation Logic
**Purpose**: Generate personalized fortunes (currently unused in main flow)

**Data Structures**:
- `OMENS`: List of fortune omens
- `ADVICE`: List of advice phrases
- `MONTH_ENERGY`: Month-based energy mappings
- `COLOR_AURA`: Color-based aura mappings

**Function**:
- `generate_fortune(name, birth_month, favorite_color, mood)`: Generates fortune text

**Note**: This module appears to be from an earlier version. Current flow displays fortunes based on user's chosen category and Arduino-printed text.

#### `arduino_serial.py` - Serial Communication Manager
**Purpose**: Handle all Arduino communication

**Class: `ArduinoSerial`**

**Methods**:
- `__init__(port, baudrate, timeout)`: Initialize connection parameters
- `connect()`: Establish serial connection
- `disconnect()`: Close serial connection
- `send_json(data_dict)`: Send JSON-formatted data
- `send_data(data_string)`: Send raw string data
- `read_response(timeout)`: Read Arduino response
- `find_arduino_port()`: Static method to auto-detect Arduino
- `list_available_ports()`: Static method to list all serial ports

**Global Functions**:
- `init_arduino(port, baudrate)`: Initialize global Arduino instance
- `get_arduino()`: Get global Arduino instance

**Auto-Detection Logic**:
Scans for common Arduino identifiers:
- Arduino, CH340, CH341, CP2102, FTDI, FT232
- ttyUSB, ttyACM, cu.usb, usbserial, usbmodem

#### `arduino_data.py` - Data Serialization
**Purpose**: Format user data for Arduino transmission

**Functions**:
- `get_user_data(session_data)`: Extract and organize session data
- `format_for_arduino_json(session_data)`: Compact JSON string
- `format_for_arduino_simple(session_data)`: Pipe-delimited key:value
- `format_for_arduino_csv(session_data)`: CSV format
- `print_data_summary(session_data)`: Console debugging output

**Data Cleaning**:
- Removes empty values
- Only sends relevant data per category path

#### `find_arduino.py` - Port Detection Utility
**Purpose**: Standalone tool to identify Arduino port

**Usage**: `python find_arduino.py`

**Output**:
- Lists all serial ports
- Highlights likely Arduino devices
- Provides manual configuration instructions
- Shows port detection tips

### Template System

#### `base.html` - Base Template
**Features**:
- HTML5 structure
- Virtual keyboard implementation
- JavaScript for keyboard interaction
- Common styling imports

**Virtual Keyboard**:
- Shows on text input focus
- Touch-optimized buttons
- Positioned right-side, vertically centered
- Supports: a-z, space (+), backspace (⌫), enter

#### Step Templates
Each step template extends `base.html` and includes:
- Form with appropriate fields
- Audio playback JavaScript
- Content from `content.py`
- Conditional rendering based on user choices

**Conditional Content Example**:
`loveStep2.html` renders different content based on `love_answer`:
- `"has_feelings"` → "What is your favourite feature of your love?"
- `"searching"` → "Name the feature that you look for in a partner."

### Static Assets Organization

#### Audio Files
- **Format**: WAV (uncompressed for quality)
- **Organization**: Folders by interaction step
- **Playback**: JavaScript in templates
- **Selection**: Some random, some conditional on user choices

#### Images
- **Formats**: PNG (animations), JPEG (photos), MP4 (video)
- **Purpose**: Visual feedback, animations, icons
- **Examples**:
  - Fortune/Love/Guidance/Surprise icon loops
  - "Start The Ritual" animation frames
  - Fingerprint scanning visualization

#### Fonts
- **dogicapixel.otf**: Custom pixel font for retro/mystical aesthetic

#### CSS
- **style.css**: All styling for kiosk interface
- Touch-optimized button sizes
- Full-screen layouts
- Animation keyframes

## 🏗️ Project Structure

```
fortune-teller/
├── app.py                      # Main Flask application & routing
├── content.py                  # Centralized content management
├── fortunes.py                 # Fortune generation logic
├── arduino_serial.py           # Serial communication with Arduino
├── arduino_data.py             # Data serialization for Arduino
├── find_arduino.py             # Utility to detect Arduino port
├── requirements.txt            # Python dependencies
├── static/
│   ├── style.css              # CSS styling
│   ├── fonts/                 # Custom fonts
│   ├── images/                # Visual assets & animations
│   └── audio/                 # Audio files organized by flow
│       ├── name/              # Step 1 audio
│       ├── step2/             # Category selection audio
│       ├── step3/             # Fingerprint ritual audio
│       ├── fingerprint/       # Fingerprint animation audio
│       ├── result/            # Final fortune audio
│       ├── love/              # Love category audio
│       ├── loveStep1/         # Love path step 1 audio
│       ├── loveStep2/         # Love path step 2 audio
│       ├── guidance/          # Guidance category audio
│       ├── guidanceStep1/     # Guidance path step 1 audio
│       ├── guidanceStep2/     # Guidance path step 2 audio
│       ├── fortune/           # Fortune category audio
│       ├── fortuneStep1/      # Fortune path step 1 audio
│       ├── fortuneStep2/      # Fortune path step 2 audio
│       ├── surprise/          # Surprise category audio
│       ├── surpriseStep1/     # Surprise path step 1 audio
│       └── surpriseStep2/     # Surprise path step 2 audio
└── templates/
    ├── base.html              # Base template with virtual keyboard
    ├── start.html             # Landing page
    ├── step1.html             # Step 1: Name input
    ├── step2.html             # Step 2: Category selection
    ├── step3.html             # Step 3: Fingerprint ritual
    ├── animation.html         # Category transition animation
    ├── fingerprint_animation.html  # Fingerprint scanning animation
    ├── result.html            # Final fortune display
    ├── loveStep1.html         # Love path: Step 1
    ├── loveStep2.html         # Love path: Step 2
    ├── guidanceStep1.html     # Guidance path: Step 1
    ├── guidanceStep2.html     # Guidance path: Step 2
    ├── fortuneStep1.html      # Fortune path: Step 1
    ├── fortuneStep2.html      # Fortune path: Step 2
    ├── surpriseStep1.html     # Surprise path: Step 1
    └── surpriseStep2.html     # Surprise path: Step 2
```

## 🏛️ System Architecture

### Overview
The Fortune Cookie is a **hardware-software hybrid interactive installation** that combines:
- **Flask web application** running on Raspberry Pi (or local computer)
- **Arduino microcontroller** controlling physical hardware (lid mechanisms, sensors, etc.)
- **Touch-screen kiosk interface** for user interaction
- **Serial communication** between Python and Arduino via USB/UART

### Architecture Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERACTION                      │
│              (Touch Screen / Kiosk Mode)                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FLASK WEB APPLICATION                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  app.py: Routes & Session Management              │  │
│  │  • Multi-step form flow                           │  │
│  │  • 4 branching paths (Love/Guidance/Fortune/      │  │
│  │    Surprise)                                       │  │
│  │  • Audio playback coordination                    │  │
│  │  • Arduino data transmission                      │  │
│  └─────┬──────────────────────────────┬──────────────┘  │
│        │                              │                 │
│        ▼                              ▼                 │
│  ┌─────────────────┐          ┌──────────────────┐     │
│  │  content.py     │          │  fortunes.py     │     │
│  │  Centralized    │          │  Fortune         │     │
│  │  text content   │          │  generation      │     │
│  └─────────────────┘          └──────────────────┘     │
│        │                                                │
│        ▼                                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Templates (Jinja2)                              │  │
│  │  • base.html: Virtual keyboard                   │  │
│  │  • Multi-step forms                              │  │
│  │  • Conditional content rendering                 │  │
│  │  • Audio playback scripts                        │  │
│  └──────────────────────────────────────────────────┘  │
│        │                                                │
│        ▼                                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Static Assets                                    │  │
│  │  • CSS styling                                    │  │
│  │  • Audio files (WAV)                              │  │
│  │  • Images & animations (PNG, JPEG, MP4)          │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ USB/UART Serial
                     │ (9600 baud)
                     ▼
┌─────────────────────────────────────────────────────────┐
│          ARDUINO SERIAL COMMUNICATION                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  arduino_serial.py: ArduinoSerial Class           │  │
│  │  • Auto-detection of Arduino port                 │  │
│  │  • Serial connection management                   │  │
│  │  • JSON message transmission                      │  │
│  │  • Response handling                              │  │
│  └────────────────────┬──────────────────────────────┘  │
│                       │                                  │
│  ┌───────────────────▼──────────────────────────────┐  │
│  │  arduino_data.py: Data Serialization             │  │
│  │  • Extract user data from Flask session           │  │
│  │  • Format as JSON (compact)                       │  │
│  │  • Alternative formats: CSV, simple key:value     │  │
│  └───────────────────────────────────────────────────┘  │
│                       │                                  │
│  ┌───────────────────▼──────────────────────────────┐  │
│  │  find_arduino.py: Port Detection Utility         │  │
│  │  • Lists all serial ports                         │  │
│  │  • Identifies Arduino devices                     │  │
│  │  • Troubleshooting helper                         │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              ARDUINO HARDWARE CONTROLLER                 │
│  • Receives JSON data from Flask                        │
│  • Controls physical mechanisms (lid, lights, etc.)     │
│  • Sends acknowledgment back to Flask                   │
│  • Reads from sensors (if applicable)                   │
└─────────────────────────────────────────────────────────┘
```

## 🎯 How It Works

### User Journey Flow

```
START
  │
  ├─→ [Start Page] "The Great Cookie"
  │
  ├─→ [Step 1] Enter Name
  │     • Text input with virtual keyboard
  │     • Random audio plays from name folder
  │     • Stores: session['name']
  │
  ├─→ [Step 2] Category Selection
  │     • 4 buttons: Love / Guidance / Fortune / Surprise
  │     • Stores: session['category']
  │     • Plays category-specific audio
  │
  ├─→ [Animation] Category transition
  │     • Visual feedback for selected path
  │
  ├─→ [Path-Specific Step 1] Multiple choice question
  │     • Different question per category
  │     • Love: "Do you have a love interest?"
  │     • Guidance: "Are you enlightened?"
  │     • Fortune: "Do you consider yourself lucky?"
  │     • Surprise: "Do you have any pets?"
  │     • Stores: session['[category]_answer']
  │
  ├─→ [Path-Specific Step 2] Text input question
  │     • Conditional content based on Step 1 answer
  │     • Virtual keyboard for text input
  │     • Stores: session['[category]_question']
  │
  ├─→ [Step 3] "Start the Ritual"
  │     • "Fingerprint" button
  │
  ├─→ [Fingerprint Animation]
  │     • Visual scanning effect
  │     • Arduino data transmission happens here
  │     • Sends all collected user data to Arduino
  │
  ├─→ [Result Page] "Take Your Fortune"
  │     • Display personalized fortune
  │     • Physical fortune cookie printed/dispensed (Arduino)
  │     • "Ask Again" button to restart
  │
  └─→ Loop back to START
```

### Data Flow

1. **Session Management**
   - Flask session stores all user inputs as they progress
   - Session data structure:
     ```python
     {
       'name': str,
       'category': 'love' | 'guidance' | 'fortune' | 'surprise',
       'love_answer': str,        # Multiple choice from Step 1
       'love_question': str,      # Text input from Step 2
       'guidance_answer': str,
       'guidance_question': str,
       'fortune_answer': str,
       'fortune_question': str,
       'surprise_answer': str,
       'surprise_question': str
     }
     ```

2. **Arduino Communication**
   - When user clicks "Fingerprint" button:
     - `get_user_data()` extracts relevant session data
     - `format_for_arduino_json()` creates compact JSON
     - `arduino.send_json()` transmits via serial
     - Arduino controls physical hardware based on received data
   
3. **Content Rendering**
   - All text is centralized in `content.py`
   - Templates retrieve content via `get_content(page_name)`
   - Enables easy text updates without touching HTML

### Audio System

- **Automatic playback** on each page load
- **Conditional audio** based on user choices
- Audio files organized by interaction flow
- Random selection from pools when applicable

### Virtual Keyboard

- **Built into base template** (`base.html`)
- **Touch-optimized** for kiosk mode
- Appears when text input is focused
- Positioned on right side of screen
- Supports: letters, space, backspace, enter (submit)

## 🔌 Arduino Integration

### Setup Requirements

1. **Hardware**: Arduino board (Uno, Mega, Nano, etc.)
2. **Connection**: USB cable from Arduino to computer/Raspberry Pi
3. **Baud Rate**: Must match both sides (default: 9600)

### Finding Your Arduino Port

Run the detection utility:
```bash
python find_arduino.py
```

This will:
- List all serial ports
- Identify likely Arduino devices
- Provide recommended port path

### Manual Port Configuration

Edit `app.py` line 18:
```python
# Auto-detect (recommended)
arduino_connection = init_arduino(port=None, baudrate=9600)

# Or specify manually
arduino_connection = init_arduino(port='/dev/ttyUSB0', baudrate=9600)
```

Common port names:
- **macOS**: `/dev/cu.usbserial*` or `/dev/cu.usbmodem*`
- **Linux**: `/dev/ttyUSB0` or `/dev/ttyACM0`
- **Windows**: `COM3`, `COM4`, `COM5`, etc.

### Data Formats Sent to Arduino

The app sends user data in **JSON format** by default:
```json
{"name":"Alice","category":"love","love_answer":"has_feelings","love_question":"their smile"}
```

**Alternative formats available** via API endpoint `/api/arduino-data?format=`:
- `json` (default): Compact JSON
- `simple`: Key-value pairs → `name:Alice|category:love|love_answer:has_feelings`
- `csv`: Comma-separated → `Alice,love,has_feelings,their smile`

### Arduino Code Requirements

Your Arduino sketch should:
1. Initialize serial at 9600 baud: `Serial.begin(9600);`
2. Read incoming JSON: `String data = Serial.readStringUntil('\n');`
3. Parse JSON (use ArduinoJson library)
4. Control hardware based on received data
5. Optionally send acknowledgment back

Example Arduino structure:
```cpp
#include <ArduinoJson.h>

void setup() {
  Serial.begin(9600);
  // Initialize hardware (servos, LEDs, etc.)
}

void loop() {
  if (Serial.available() > 0) {
    String jsonData = Serial.readStringUntil('\n');
    
    StaticJsonDocument<512> doc;
    deserializeJson(doc, jsonData);
    
    const char* name = doc["name"];
    const char* category = doc["category"];
    
    // Control hardware based on data
    // e.g., open lid, print fortune, flash LEDs
    
    Serial.println("ACK"); // Send acknowledgment
  }
}
```

## 💡 Tips

- **Deactivate the virtual environment** when you're done:
  ```bash
  deactivate
  ```

- **Update dependencies** if needed:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

- **Check if virtual environment is active**: Look for `(venv)` at the start of your terminal prompt

## 📝 Content Management

All user-facing text (titles, labels, button text, placeholders) is centralized in `content.py`. This makes it easy to update text without touching HTML templates.

**To change any text displayed in the app:**
1. Open `content.py`
2. Find the page/step you want to modify
3. Update the text values
4. Save and refresh your browser

📖 See `CONTENT_GUIDE.md` for detailed documentation on managing content.

## ⚙️ Configuration

The application runs on:
- **Host**: 0.0.0.0 (accessible from any network interface)
- **Port**: 5001
- **Debug Mode**: Enabled (automatically reloads on code changes)

⚠️ **Note**: Change the `secret_key` in `app.py` before deploying to production!

## 🐛 Troubleshooting

**Virtual environment not activating?**
- Make sure you're in the correct directory
- Try: `source venv/bin/activate` or `source env/bin/activate`

**Port 5001 already in use?**
- Edit `app.py` and change the port number in the last line
- Or stop any other processes using port 5001

**Module not found errors?**
- Make sure your virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

- or use: `python3 -m pip install -r requirements.txt`


## 🚀 Deployment Considerations

### Kiosk Mode Setup (Raspberry Pi)

The Fortune Cookie app includes complete kiosk mode support for Raspberry Pi installations. This provides a full-screen, touch-optimized experience with no visible cursor or browser UI elements.

#### Quick Setup (Recommended)

1. **Run the setup script** (one-time configuration):
   ```bash
   cd fortune-teller
   ./setup-kiosk.sh
   ```
   
   This script will:
   - Install required packages (unclutter, chromium-browser, etc.)
   - Configure system settings to prevent screen blanking
   - Set up a systemd service for auto-start
   - Optionally enable auto-start on boot

2. **The setup script will ask if you want to:**
   - Enable auto-start on boot (recommended for kiosks)
   - Start the kiosk service immediately

#### Manual Setup

If you prefer to set up manually:

1. **Install required packages**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y unclutter x11-xserver-utils chromium-browser netcat-openbsd
   ```

2. **Configure screen settings** (prevents screen blanking):
   ```bash
   echo "xset s off" >> ~/.xprofile
   echo "xset -dpms" >> ~/.xprofile
   echo "xset s noblank" >> ~/.xprofile
   chmod +x ~/.xprofile
   ```

3. **Set up systemd service**:
   ```bash
   # Edit the service file with your actual paths
   sudo nano fortune-cookie-kiosk.service
   
   # Copy to systemd directory
   sudo cp fortune-cookie-kiosk.service /etc/systemd/system/
   sudo systemctl daemon-reload
   
   # Enable auto-start on boot
   sudo systemctl enable fortune-cookie-kiosk.service
   
   # Start the service
   sudo systemctl start fortune-cookie-kiosk.service
   ```

#### Kiosk Mode Features

The kiosk mode setup provides:
- ✅ **Full-screen browser** - No address bar, tabs, or browser UI
- ✅ **Hidden cursor** - Cursor automatically hides (unclutter)
- ✅ **No screen blanking** - Display stays on
- ✅ **Auto-start on boot** - App launches automatically when Pi boots
- ✅ **Auto-restart** - Service automatically restarts if it crashes
- ✅ **Touch-optimized** - Designed for touchscreen interaction only

#### Managing the Kiosk Service

**Start the kiosk**:
```bash
sudo systemctl start fortune-cookie-kiosk.service
```

**Stop the kiosk**:
```bash
sudo systemctl stop fortune-cookie-kiosk.service
```

**Or use the exit script**:
```bash
./exit-kiosk.sh
```

**Check status**:
```bash
sudo systemctl status fortune-cookie-kiosk.service
```

**View logs**:
```bash
journalctl -u fortune-cookie-kiosk.service -f
```

**Disable auto-start**:
```bash
sudo systemctl disable fortune-cookie-kiosk.service
```

**Enable auto-start**:
```bash
sudo systemctl enable fortune-cookie-kiosk.service
```

#### Exiting Kiosk Mode

If you need to exit kiosk mode while it's running:

1. **Switch to a TTY** (virtual terminal):
   - Press `Ctrl+Alt+F1` (or F2-F6) to switch to a text console
   - Log in and run: `sudo systemctl stop fortune-cookie-kiosk.service`
   - Press `Ctrl+Alt+F7` (or F8) to return to the desktop

2. **SSH into the Pi** (if SSH is enabled):
   ```bash
   ssh pi@raspberrypi
   sudo systemctl stop fortune-cookie-kiosk.service
   ```

3. **Use the exit script** (if you have terminal access):
   ```bash
   ./exit-kiosk.sh
   ```

#### Manual Kiosk Launch (Testing)

To test kiosk mode without the service:

```bash
cd fortune-teller
./start-kiosk.sh
```

This will:
- Hide the cursor
- Start the Flask app
- Launch Chromium in full kiosk mode

Press `Ctrl+C` in the terminal to stop.

#### Troubleshooting Kiosk Mode

**Cursor still visible?**
- Make sure `unclutter` is installed: `sudo apt-get install unclutter`
- Check if unclutter is running: `ps aux | grep unclutter`

**Screen goes blank?**
- Check `.xprofile` settings: `cat ~/.xprofile`
- Manually run: `xset s off && xset -dpms && xset s noblank`

**Browser doesn't start?**
- Check if Flask is running: `curl http://localhost:5001`
- Check service logs: `journalctl -u fortune-cookie-kiosk.service -n 50`

**Service won't start?**
- Check service file paths are correct
- Verify user permissions
- Check logs: `journalctl -u fortune-cookie-kiosk.service`

**Chromium shows error dialogs?**
- The startup script includes flags to suppress dialogs
- Check that all Chromium flags are being applied

### Production Recommendations

#### Security
⚠️ **Change the Flask secret key** in `app.py`:
```python
app.secret_key = 'your-long-random-secret-key-here'
```

Generate secure key:
```python
import secrets
print(secrets.token_hex(32))
```

#### Performance
- **Disable debug mode** for production:
  ```python
  app.run(host="0.0.0.0", port=5001, debug=False)
  ```

- **Use production WSGI server** (Gunicorn):
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:5001 app:app
  ```

#### Network Access
- **Local only**: Keep `host="0.0.0.0"` with firewall rules
- **External access**: Use reverse proxy (nginx) with HTTPS
- **Kiosk mode**: Usually runs on localhost (no network needed)

### Hardware Requirements

**Minimum**:
- Raspberry Pi 3B+ or equivalent
- 2GB RAM
- Touchscreen display
- USB port for Arduino
- SD card (16GB+)

**Recommended**:
- Raspberry Pi 4 (4GB RAM)
- Official 7" touchscreen or larger
- Powered USB hub for Arduino (if using power-hungry peripherals)
- 32GB SD card

**Arduino**:
- Any Arduino board (Uno, Mega, Nano, etc.)
- Adequate power for servos/motors/LEDs
- USB cable for serial connection

## 🔧 Technical Architecture Decisions

### Why Flask?
- **Lightweight**: Perfect for embedded systems (Raspberry Pi)
- **Simple routing**: Easy to understand flow
- **Built-in sessions**: Stateful user journeys
- **Template engine**: Jinja2 for dynamic content
- **Quick development**: Rapid prototyping for installations

### Why Serial Communication?
- **Reliable**: UART is proven, stable protocol
- **Simple**: No complex networking required
- **Direct control**: Arduino controls hardware directly
- **Debugging**: Easy to monitor with serial console
- **Cross-platform**: Works on Windows/Mac/Linux/Raspberry Pi

### Why Session-Based State?
- **User isolation**: Each session is independent
- **Persistence**: Data survives navigation
- **Simplicity**: No database needed
- **Privacy**: Sessions expire, no permanent storage

### Why JSON for Arduino Data?
- **Standard**: Well-supported format
- **Structured**: Easy to parse with ArduinoJson library
- **Compact**: Minimal overhead for serial transmission
- **Flexible**: Easy to add/remove fields
- **Alternative formats**: Simple/CSV available if needed

### Why Virtual Keyboard?
- **Touch-first**: Designed for kiosk touchscreen
- **No physical keyboard**: Reduces hardware footprint
- **Customizable**: Only needed characters
- **Consistent UX**: Always available when needed

### Why Centralized Content?
- **Maintainability**: Update text without touching code/HTML
- **Consistency**: Single source of truth
- **Future-proof**: Easy to add localization
- **Non-technical edits**: Writers can edit without developer

## 🎨 Design Patterns Used

### **Multi-Page Form (Wizard Pattern)**
- User journey broken into small steps
- Progressive disclosure of information
- Session maintains state between steps
- Clear navigation flow

### **Template Inheritance**
- `base.html` provides common structure
- Step templates extend base
- DRY principle: virtual keyboard defined once

### **Content-View Separation**
- `content.py` separates data from presentation
- Templates are logic-light
- Easy to change copy without touching HTML

### **Factory Pattern (Arduino Connection)**
- `init_arduino()` creates singleton instance
- `get_arduino()` retrieves global instance
- Initialized once at app startup

### **Strategy Pattern (Data Formats)**
- Multiple serialization strategies (JSON/CSV/Simple)
- Same data, different formats
- Switchable via API parameter

## 🔍 Debugging & Development Tips

### View Serial Communication
Monitor Arduino data in real-time:
```bash
python -m serial.tools.miniterm /dev/ttyUSB0 9600
```

### Flask Debug Output
Console shows:
- Route access logs
- Arduino connection status
- Data transmission confirmations
- Session data summaries

### Check Session Data
Add to any route handler:
```python
print(f"Session data: {dict(session)}")
```

### Test Without Arduino
App gracefully handles missing Arduino:
- Connection attempts on startup
- Falls back to console logging
- Warns but doesn't crash
- Full web flow still works

### Inspect Arduino Data
Visit API endpoint in browser:
```
http://localhost:5001/api/arduino-data?format=json
http://localhost:5001/api/arduino-data?format=simple
http://localhost:5001/api/arduino-data?format=csv
```

### CSS/JS Changes
Debug mode auto-reloads Python changes, but for static files:
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows/Linux)
- Or add cache-busting: `?v=2` to asset URLs

## 📖 Resources Directory

The `/resources` folder contains:
- **`01 Raxter Code/`**: Original Arduino code and scripts
  - `fortune_game_lid.py`: Earlier Python version
  - `great_arduino/`: Arduino sketch (.ino file)
  - `TGC_arduino_control.py`: Arduino control script
- **`Audio Selects/`**: Full library of audio files (WAV)
  - Master audio collection before organizing into `/static/audio/`
- **Image Assets**: Animation frames for fortune icons
  - Fortune Icon Loop
  - Guidance Icon Loop
  - Love Icon Loop
  - Surprise Icon Loop
  - Start The Ritual sequences

**Note**: These are source/reference materials. The active app uses files in `/fortune-teller/static/`.

## 🆘 Common Issues & Solutions

### "No Arduino found"
1. Check USB connection
2. Run `python find_arduino.py`
3. Check Arduino drivers installed
4. Try manually specifying port in `app.py`

### "Port already in use"
```bash
# Find process using port 5001
lsof -i :5001

# Kill process
kill -9 <PID>
```

### Audio not playing
- Check browser console for errors
- Ensure WAV files are in correct location
- Modern browsers require user interaction before audio
- Check volume/mute settings

### Virtual keyboard not appearing
- Ensure base.html is properly extended
- Check for JavaScript errors in console
- Verify text input has `type="text"`

### Session data not persisting
- Check Flask secret_key is set
- Ensure cookies are enabled
- Session expires on server restart (by design)

### Arduino not receiving data
1. Check baud rate matches (9600)
2. Verify Arduino Serial.begin(9600) in setup()
3. Monitor serial with miniterm
4. Check USB cable (data, not charging-only)
5. Try different USB port

## 📝 License

This project is for educational and entertainment purposes.

---

✨ *May your fortunes be ever in your favor!* ✨

