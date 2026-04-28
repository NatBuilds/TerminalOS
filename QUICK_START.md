# Quick Start Guide

Get your TerminalOS environment set up and running in 5 minutes.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

## First Run

You should see a main menu with options like:
- Example
- Task
- Tools
- Settings
- Device Tools (if ADB is configured)
- Logs
- Cron Scheduler

Navigate with number keys and press `0` to go back.

## Core Modules Included

### Settings
Control verbose output and view application state.

```
Main Menu → Settings
├─ Toggle Verbose Mode
└─ View Application State
```

### Example
Simple demonstration module.

```
Main Menu → Example
└─ Say Hello
```

### Tools
Example submenu structure.

```
Main Menu → Tools
├─ Option A
└─ Option B
```

### Logs
View and manage application logs.

```
Main Menu → Logs
├─ View current session logs
├─ View session statistics
├─ View error summary
├─ Search logs
├─ View all log files
├─ Show logs directory
└─ Clear old logs
```

### Cron Scheduler
Schedule recurring tasks.

```
Main Menu → Cron Scheduler
├─ Create New Task
├─ View Task Details
├─ Edit Task
├─ Delete Task
├─ Toggle Task Status
└─ View All Tasks
```

## Android Device Setup (Optional)

### Prerequisites

Install ADB (Android Debug Bridge):

```bash
# Windows (Chocolatey)
choco install android-sdk

# macOS (Homebrew)
brew install android-platform-tools

# Linux
sudo apt-get install android-tools-adb

# Or: Download from https://developer.android.com/studio/releases/platform-tools
```

### Connect a Device

1. Enable USB debugging on your Android device
   - Settings → Developer Options → USB Debugging
2. Connect via USB
3. Accept the ADB connection prompt on your device
4. Run `adb devices` to verify

### Test Device Tools

```bash
python run.py
# Navigate to: Main Menu → Device Tools
```

## Image Processing Setup (Optional)

### OpenCV

Already included in `requirements.txt`. If missing:

```bash
pip install opencv-python>=4.10.0.84
```

### Tesseract OCR

For text extraction from images:

```bash
# Windows (Chocolatey)
choco install tesseract

# macOS
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr

# Then install Python wrapper
pip install pytesseract>=0.3.13
```

## Try the Examples

### 1. Device Screenshot & Analysis

If you have an Android device connected:

```bash
python run.py
# Navigate to: Device Tools → ADB Screenshot and read
```

This demonstrates:
- ADB screenshot capture
- OpenCV image processing (grayscale, blur, edges)
- Tesseract OCR text extraction

### 2. View Application Logs

```bash
python run.py
# Navigate to: Logs → View current session logs
```

All application activity is automatically logged.

### 3. Schedule a Task

```bash
python run.py
# Navigate to: Cron Scheduler → Create New Task
# Task name: Test Task
# Cron expression: */1 * * * *  (every minute)
# Command: task:hello_world
```

## Configuration

Edit `app/config.json` to customize behavior:

```json
{
  "verbose": false,
  "adb": {
    "adb_executable": "adb",
    "device_serial": "",
    "timeout": 30
  },
  "ocr": {
    "tesseract_cmd": "tesseract",
    "language": "eng",
    "psm": 3,
    "oem": 3,
    "timeout": 30
  },
  "llm": {
    "provider": "lm_studio",
    "base_url": "http://localhost:1234",
    "chat_endpoint": "/v1/chat/completions",
    "model": "your-model",
    "api_key": "not-needed",
    "timeout": 30
  }
}
```

## Create Your First Module

### 1. Create the File

Create `app/modules/hello/controller.py`:

```python
from app.core import status

def greet() -> None:
    status.success("Hello from my module!")

def register(menu) -> None:
    menu.add("Greet", greet)
```

### 2. Run the App

```bash
python run.py
```

Your new module appears in the menu automatically!

### 3. Edit and See Changes

Edit `greet()` and press menu selection again - changes appear without restarting!

## Common Tasks

### List Connected Devices

```python
from app.libraries import ADBController

adb = ADBController()
for device in adb.devices():
    print(f"Device: {device.serial} ({device.state})")
```

### Capture Screenshot

```python
from app.libraries import ADBController

adb = ADBController()
adb.screenshot("screenshot.png")
```

### Process Image

```python
from app.libraries import OpenCVImageTools

cv = OpenCVImageTools()
image = cv.load_image("screenshot.png")
gray = cv.to_grayscale(image)
cv.save_image("gray.png", gray)
```

### Extract Text

```python
from app.libraries import TesseractOCR

ocr = TesseractOCR()
text = ocr.extract_text("screenshot.png")
print(text)
```

## Troubleshooting

### "adb: command not found"

Make sure ADB is installed and in your PATH:
- Windows: Check PATH environment variable includes Android SDK
- macOS/Linux: Verify installation with `which adb`

### "No devices found"

1. Check device is connected: `adb devices`
2. Enable USB debugging on device
3. Accept ADB prompt on device
4. Try `adb kill-server && adb devices` to reset

### "ModuleNotFoundError: No module named 'colorama'"

Run: `pip install -r requirements.txt`

### Module doesn't appear in menu

1. Verify `app/modules/<name>/controller.py` exists
2. Check `register(menu)` function exists
3. Enable verbose mode to see errors
4. Check logs in `logs/` directory

## Next Steps

- **[README.md](README.md)** - Full framework documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines
- **[LIBRARIES_GUIDE.md](LIBRARIES_GUIDE.md)** - API reference
- **[LOGGING_GUIDE.md](LOGGING_GUIDE.md)** - Logging system
- **[CRON_SCHEDULER_QUICKSTART.md](CRON_SCHEDULER_QUICKSTART.md)** - Task scheduling

## Getting Help

1. Enable verbose in Settings menu
2. Check `logs/` directory for detailed output
3. Review example modules in `app/modules/`
4. Check documentation files

---

**Happy building!** 🚀

