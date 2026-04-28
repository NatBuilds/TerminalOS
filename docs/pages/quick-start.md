# Quick Start Guide

Get TerminalOS running in 5 minutes.

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python run.py
```

That's it! You should see the main menu.

## First Steps in the App

### 1. Explore the Settings Menu

- Navigate to **Settings**
- Toggle **Verbose Mode** to see debug output
- View current configuration

### 2. Check the Examples

- Navigate to **Tools** for example submenu structure
- Navigate to **Example** for a simple "Hello" action
- These are great templates for building your own modules

### 3. View Application Logs

- Navigate to **Logs** to see session history
- Check the `logs/` folder for detailed session files

## Creating Your First Module

Create a new file at `app/modules/helloworld/controller.py`:

```python
from app.core import status

def greet() -> None:
    status.success("Hello, World!")

def register(menu) -> None:
    menu.add("Say Hello", greet)
```

Save the file, run `python run.py`, and your new menu item appears automatically!

## Next Steps

- **[Architecture Guide](architecture.md)** - Understand the module system
- **[API Reference](api-reference.md)** - See all available libraries
- **[Development Guide](development.md)** - Build advanced features
- **[Full README](https://github.com/NatBuilds/TerminalOS/blob/main/README.md)** - Complete documentation

## Android ADB Setup (Optional)

If you want to use Android device automation:

### Install ADB

**Windows (via Chocolatey):**
```bash
choco install android-sdk
```

**macOS:**
```bash
brew install android-platform-tools
```

**Linux:**
```bash
sudo apt-get install android-tools-adb
```

Or download from: [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools)

### Configure in TerminalOS

The config is auto-created at `app/config.json`. Verify the ADB path:

```json
{
  "adb": {
    "adb_executable": "adb",
    "device_serial": "",
    "timeout": 30
  }
}
```

### Enable USB Debugging

On your Android device:
1. Settings → Developer Options → USB Debugging (Enable)
2. Connect device via USB
3. Accept ADB prompt on device
4. Navigate to **Device Tools** in TerminalOS

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'colorama'` | Run `pip install -r requirements.txt` again |
| Module not showing in menu | Verify `controller.py` exists and `register(menu)` doesn't crash |
| ADB not found | Install Android Platform Tools or update ADB path in `config.json` |
| No debug output | Enable Verbose Mode in Settings menu |
| Permission errors | Run terminal as administrator |

## Configuration

TerminalOS auto-creates `app/config.json` with sensible defaults:

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

Changes are picked up automatically on next app run.

## What's Next?

- ✅ You're running TerminalOS!
- 📖 Read the [Architecture Guide](architecture.md) to understand the framework
- 🛠️ Build your first advanced module using the [Development Guide](development.md)
- 📚 Explore the [API Reference](api-reference.md) for all available libraries
- 🤖 Check out Android automation in [Device Tools](https://github.com/NatBuilds/TerminalOS/tree/main/app/modules/device_tools)

---

**[← Back to Home](/)** | **[Architecture Guide →](architecture.md)**

