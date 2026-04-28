# Architecture Guide for Developers & AI Agents

## Overview

TerminalOS is a modular Python CLI framework designed for extensibility. This guide explains the architecture for developers and AI agents implementing new features.

## Installation

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Core Concepts

- **Modular Design**: Features live in `app/modules/*/controller.py`
- **Dynamic Discovery**: Each loop scans for modules and reloads them
- **Live Reloading**: Code changes picked up on next menu render (no restart needed)
- **Clean Separation**: UI, status, config, and business logic are isolated
- **Android Integration**: ADB controller for device automation included

## Module Discovery Contract

Every module in `app/modules/*/controller.py` must:

1. Export a `register(menu) -> None` function
2. Add menu items using `menu.add("Label", handler)`
3. Use only no-arg callables as handlers
4. Return to allow automatic reloading

Example:

```python
from app.core import status

def my_action() -> None:
    status.success("Action executed!")

def register(menu) -> None:
    menu.add("My Action", my_action)
```

## Layer Architecture

### Presentation Layer (`app/core/`)
- `menu.py` - Menu system with no-arg callable handlers
- `ui.py` - Console output, banners, clear screen
- `status.py` - Centralized logging (info, warning, error, success, debug)

### Configuration Layer (`app/core/`)
- `config.py` - Configuration file management with auto-healing
- `cron_runtime.py` - Scheduled task execution

### Business Logic Layers
- `app/modules/*/` - Feature modules (auto-discovered)
- `app/modules/*/service.py` - Business logic (optional, import in controller)
- `app/libraries/*/` - Shared utilities and integrations

### Libraries Provided
- `adb/` - Android device control (30+ methods)
- `opencv/` - Image processing (20+ methods)
- `ocr/` - Text extraction via Tesseract (8+ methods)
- `logging/` - File-based session logging
- `cron/` - Task scheduling engine
- `text/` - Text manipulation utilities
- `files/` - File operations

## Development Patterns

### Adding a New Module

1. Create `app/modules/<name>/` directory
2. Create `app/modules/<name>/controller.py`:

```python
from app.core import status

def handler_one() -> None:
    status.info("Handler 1 executed")

def handler_two() -> None:
    status.success("Handler 2 executed")

def register(menu) -> None:
    menu.add("Option 1", handler_one)
    menu.add("Option 2", handler_two)
```

3. Add to main menu - it's auto-discovered!

### Using Libraries

```python
from app.libraries import ADBController, OpenCVImageTools, TesseractOCR
from app.core import status

def my_feature() -> None:
    adb = ADBController()
    if not adb.is_available():
        status.error("ADB not available")
        return
    
    devices = adb.devices()
    status.success(f"Found {len(devices)} devices")
```

### Creating Submenus

```python
def submenu_handler() -> None:
    # This creates a submenu
    submenu = Menu("Submenu Title")
    submenu.add("Sub-option 1", handler_one)
    submenu.add("Sub-option 2", handler_two)
    submenu.show()

def register(menu) -> None:
    menu.add("Open Submenu", submenu_handler)
```

### Business Logic in Services

Keep controllers thin, put logic in services:

```python
# app/modules/mymodule/service.py
def process_data(data):
    # Complex business logic here
    return result

# app/modules/mymodule/controller.py
from .service import process_data
from app.core import status

def handle_processing() -> None:
    result = process_data(some_data)
    status.success(f"Processed: {result}")

def register(menu) -> None:
    menu.add("Process", handle_processing)
```

## Configuration & State Management

### Accessing Configuration

```python
from app.core import config

# Get values
verbose_enabled = config.get_verbose()
adb_timeout = config.get_adb_timeout()

# Set values
config.toggle_verbose()
config.set_adb_timeout(60)
```

### Configuration File

Located at `app/config.json` - auto-created with defaults.

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
  "cron_tasks": []
}
```

### Auto-Healing

The config system automatically:
- Creates missing files with defaults
- Repairs invalid JSON
- Adds missing keys
- Maintains backward compatibility

## Android ADB Integration

### Basic Usage

```python
from app.libraries import ADBController

adb = ADBController()

# List devices
for device in adb.devices():
    print(f"{device.serial}: {device.state}")

# Device interaction
adb.tap(100, 200)              # Tap coordinates
adb.talk("Text input")          # Send text
adb.press("KEYCODE_HOME")       # Press key
adb.swipe(100, 100, 500, 500)  # Swipe

# App management
adb.open_app("com.example.app")
adb.is_app_running("com.example.app")

# File operations
adb.screenshot("screenshot.png")
adb.push("/local/file", "/device/path")
adb.pull("/device/file", "/local/path")
```

### ADB + OpenCV + OCR Workflow

See `app/modules/screenshot_analyzer/controller.py` for complete example combining all three libraries.

## Logging System

### Automatic Logging

All status calls are automatically logged to `logs/session_YYYYMMDD_HHMMSS.log`:

```python
from app.core import status

status.info("Info message")       # Logged
status.warning("Warning")         # Logged
status.error("Error")             # Logged
status.success("Success")         # Logged
status.debug("Debug")             # Logged if verbose enabled
```

### Manual Logging

```python
from app.libraries.logging import log_info, log_error

log_info("Custom message")
log_error("Error with context", device="device_id")
```

### Session Statistics

Automatically tracked and written on app exit:

```
================================================================================
Session Summary
================================================================================
Total Messages:  127
Errors:          3
Warnings:        8
Duration:        45.3 seconds
End Time:        2026-04-28 11:12:00
================================================================================
```

## Development Workflow

### Setup
```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
python -m venv .venv
# Activate .venv (see QUICK_START.md)
pip install -r requirements.txt
```

### Development Loop
1. Create/modify module in `app/modules/<name>/controller.py`
2. Run `python run.py`
3. Select your module from menu
4. Edit code and select menu item again - changes appear instantly!
5. Enable verbose in Settings to see debug logs

### Debugging
- Check `logs/` directory for detailed application logs
- Enable verbose mode in Settings menu
- Use `status.debug()` for diagnostic output
- Watch module reload in action

### Testing
No formal test suite. Validate by:
1. Running affected menu path
2. Verifying expected status output
3. Checking logs for errors
4. Testing with real Android device if using ADB

## Dependencies

### Core Requirements
- `colorama>=0.4.6` - Colored terminal output
- `requests>=2.31.0` - HTTP requests
- `opencv-python>=4.10.0.84` - Image processing
- `pytesseract>=0.3.13` - OCR support

### System Requirements
- Python 3.12+
- ADB (optional, for Android automation)
- Tesseract (optional, for text extraction)

### Installation
```bash
pip install -r requirements.txt

# For ADB support
# Windows: choco install android-sdk
# macOS: brew install android-platform-tools
# Linux: sudo apt-get install android-tools-adb

# For Tesseract OCR
# Windows: choco install tesseract
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

## File Structure Reference

```
app/
├── main.py                    # Runtime loop and module discovery
├── config.json               # Auto-created configuration
├── core/
│   ├── menu.py              # Menu system
│   ├── ui.py                # Console rendering
│   ├── status.py            # Status logging
│   ├── config.py            # Configuration management
│   └── cron_runtime.py      # Task scheduler
├── libraries/
│   ├── adb/adb_controller.py
│   ├── opencv/image_tools.py
│   ├── ocr/tesseract_ocr.py
│   ├── logging/file_logger.py
│   ├── cron/
│   └── text/
└── modules/                 # Auto-discovered features
    ├── settings/
    ├── tools/
    ├── device_tools/
    ├── screenshot_analyzer/
    ├── cron_scheduler/
    ├── logs/
    └── example/
```

## Documentation Reference

- **README.md** - Full project overview
- **QUICK_START.md** - Get started in 5 minutes
- **CONTRIBUTING.md** - Development guidelines
- **LIBRARIES_GUIDE.md** - API reference for all libraries
- **LOGGING_GUIDE.md** - Logging system features
- **CRON_SCHEDULER_QUICKSTART.md** - Task scheduling

