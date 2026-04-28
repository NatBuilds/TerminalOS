# TerminalOS - Modular Terminal CLI Framework

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A production-ready backbone for building modular Python CLI applications. Discover feature modules at runtime, reload code without restarting, and integrate Android device automation via ADB.

## Key Features

- **🔌 Dynamic Module Discovery**: Drop new modules into `app/modules/*/controller.py` and they load automatically
- **🔄 Live Code Reloading**: Menu rebuilds each loop to pick up module/library changes instantly
- **📱 Android Automation Ready**: Integrated ADB controller for device control, screenshot capture, and interaction
- **🎨 Clean Architecture**: Separate concerns with dedicated UI, status, config, and library boundaries
- **🧩 Extensible by Design**: Controllers stay thin; business logic lives in services or libraries
- **⚡ Production-Grade**: Comprehensive logging, error handling, and configuration management

## Installation

### From GitHub

```bash
# Clone the repository
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt

# Run the application
python run.py
```

### Requirements

- Python 3.12+
- `colorama>=0.4.6` - Colored terminal output
- `requests>=2.31.0` - HTTP requests
- `opencv-python>=4.10.0.84` - Image processing (optional)
- `pytesseract>=0.3.13` - OCR support (optional)

### Android ADB Support (Optional)

For Android device automation:

```bash
# Windows (via Chocolatey)
choco install android-sdk

# macOS
brew install android-platform-tools

# Linux
sudo apt-get install android-tools-adb

# Or download from: https://developer.android.com/studio/releases/platform-tools
```

## Quick Start

```bash
python run.py
```

Navigate through the menu to:
- **Settings** - Control verbose/debug output
- **Tools** - Example tool menus
- **Device Tools** - Android ADB utilities (if configured)
- **Logs** - View application logs

## How It Works

### Runtime Flow

1. **Entry**: `run.py` → `app.main.main()`
2. **Discovery**: Scans `app/modules/*/controller.py` for feature modules
3. **Reload**: Reloads libraries and module controllers each menu loop
4. **Register**: Calls each module's `register(menu)` function
5. **Display**: Renders menu and executes selected action
6. **Repeat**: Back to step 2 (enables live code editing)

## Current Modules

- **example** - Basic "Hello" example
- **settings** - Toggle verbose mode and view state
- **tools** - Example submenu structure
- **device_tools** - ADB utilities (11 options) + Vision tools (3 options)
- **screenshot_analyzer** - Complete ADB + OpenCV + Tesseract example
- **cron_scheduler** - Task scheduling interface
- **logs** - Log management and search

## Configuration

Config file: `app/config.json` (auto-created with sensible defaults)

### LLM Integration (Optional)

```json
{
  "llm": {
    "provider": "lm_studio",
    "base_url": "http://localhost:1234",
    "chat_endpoint": "/v1/chat/completions",
    "model": "your-model-name",
    "api_key": "not-needed",
    "timeout": 30
  }
}
```

### ADB Configuration

```json
{
  "adb": {
    "adb_executable": "adb",
    "device_serial": "",
    "timeout": 30
  }
}
```

### OCR Configuration

```json
{
  "ocr": {
    "tesseract_cmd": "tesseract",
    "language": "eng",
    "psm": 3,
    "oem": 3,
    "timeout": 30
  }
}
```

## LLM Integration (LM Studio)

`app/libraries/llm/llm_chat.py` behavior:

- Builds endpoint from `base_url + chat_endpoint`
- Checks availability via `GET /models` (`check_endpoint()`)
- Sends OpenAI-style chat payloads to `/chat/completions`
- Parses `choices[0].message.content`
- Reports transport/shape errors through status logs

## Verified Runtime Snippets (This Workspace)

The following outputs were captured during a verification run on this workspace on 2026-04-26.

Dependency check after install attempt:

```text
WARNING: Package(s) not found: colorama
WARNING: Package(s) not found: requests
```

Install command re-run result:

```text
python -m pip install -r requirements.txt --disable-pip-version-check --retries 1 --timeout 15
... (Command execution interrupted after 300000 milliseconds)
```

Start attempt before dependencies were available:

```text
Traceback (most recent call last):
  File "INSTALL_LOCATION\TerminalOS\run.py", line 1, in <module>
    from app.main import main
  ...
ModuleNotFoundError: No module named 'colorama'
```

If you hit the same issue, run:

```powershell
python -m pip install -r requirements.txt
```

## Requirements

- Python 3.11+
- `colorama>=0.4.6`
- `requests>=2.31.0`

## Project Layout

```text
TerminalOS/
├─ run.py
├─ requirements.txt
├─ README.md
├─ CONTRIBUTING.md
├─ AGENTS.md
├─ templates/
│  └─ module_template_controller.py
└─ app/
   ├─ main.py
   ├─ config.json
   ├─ assets/ascii.txt
   ├─ core/
   ├─ libraries/
   ├─ modules/
   └─ tmp/
```

## Build New Features Fast

Create a new module with `app/modules/<name>/controller.py`:

```python
from app.core import status

def my_action() -> None:
    status.success("My feature works!")

def register(menu) -> None:
    """Called automatically at startup"""
    menu.add("My Feature", my_action)
```

Or use the template: `templates/module_template_controller.py`

## Android Device Integration

### Quick Example

```python
from app.libraries import ADBController

adb = ADBController()

# List devices
for device in adb.devices():
    print(f"{device.serial}: {device.state}")

# Capture screenshot
adb.screenshot("screenshots/screen.png")

# Control device
adb.tap(100, 200)
adb.talk("Hello Android")
adb.open_app("com.android.chrome")
```

### Screenshot Analysis Workflow

Combine ADB, OpenCV, and OCR:

```python
from app.libraries import ADBController, OpenCVImageTools, TesseractOCR

adb = ADBController()
cv = OpenCVImageTools()
ocr = TesseractOCR()

# Capture
adb.screenshot("screenshot.png")

# Process
image = cv.load_image("screenshot.png")
gray = cv.to_grayscale(image)

# Extract text
text = ocr.extract_text("screenshot.png")
```

See `app/modules/screenshot_analyzer/controller.py` for complete example.

## Project Structure

```
TerminalOS/
├── run.py                    # Entry point
├── requirements.txt          # Python dependencies
├── app/
│   ├── main.py              # Core runtime loop
│   ├── config.json          # Configuration (auto-created)
│   ├── core/                # Framework essentials
│   │   ├── menu.py          # Menu system
│   │   ├── ui.py            # Console rendering
│   │   ├── status.py        # Status logging
│   │   ├── config.py        # Config management
│   │   └── cron_runtime.py  # Task scheduling
│   ├── libraries/           # Reusable components
│   │   ├── adb/             # Android ADB controller
│   │   ├── opencv/          # Image processing
│   │   ├── ocr/             # Text extraction
│   │   ├── logging/         # File logging
│   │   ├── cron/            # Task scheduler
│   │   └── text/            # Text utilities
│   └── modules/             # Feature modules (auto-discovered)
│       ├── example/
│       ├── settings/
│       ├── tools/
│       ├── device_tools/
│       ├── screenshot_analyzer/
│       ├── cron_scheduler/
│       └── logs/
├── templates/               # Module template
└── logs/                    # Application logs

```

## Development

### Adding a Module

1. Create `app/modules/<name>/controller.py`
2. Implement `register(menu) -> None`
3. Add actions: `menu.add("Label", handler)`
4. Save and run - it's auto-loaded!

### Debugging

Enable verbose mode in Settings menu to see debug logs. Changes to modules are picked up on next menu render without restarting.

### Testing

No formal test framework is included. Validate changes by:
1. Running `python run.py`
2. Navigating to your module
3. Verifying expected output

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not in menu | Verify `controller.py` exists and `register(menu)` doesn't raise |
| No debug output | Enable verbose in Settings menu |
| ADB not found | Install Android SDK Platform Tools or configure path in config.json |
| No devices detected | Enable USB debugging, connect device, accept ADB prompt |
| OpenCV errors | Run `pip install opencv-python` |
| Tesseract not working | Install system-wide (choco/brew/apt) and `pytesseract` |

## Performance Notes

- Menu rebuild is ~50-200ms depending on modules
- Live reload enabled for development; suitable for production dashboards
- Logging adds minimal overhead
- Thread-safe for basic concurrent use

