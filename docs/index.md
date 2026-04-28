# TerminalOS - Modular Terminal CLI Framework

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A production-ready backbone for building modular Python CLI applications. Discover feature modules at runtime, reload code without restarting, and integrate Android device automation via ADB.

## ✨ Key Features

- **🔌 Dynamic Module Discovery** - Drop new modules into `app/modules/*/controller.py` and they load automatically
- **🔄 Live Code Reloading** - Menu rebuilds each loop to pick up module/library changes instantly
- **📱 Android Automation Ready** - Integrated ADB controller for device control, screenshot capture, and interaction
- **🎨 Clean Architecture** - Separate concerns with dedicated UI, status, config, and library boundaries
- **🧩 Extensible by Design** - Controllers stay thin; business logic lives in services or libraries
- **⚡ Production-Grade** - Comprehensive logging, error handling, and configuration management

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # macOS/Linux
pip install -r requirements.txt

# Run
python run.py
```

## 📚 Documentation

- **[Quick Start Guide](pages/quick-start.md)** - Get running in 5 minutes
- **[Architecture Guide](pages/architecture.md)** - Deep dive into module system
- **[API Reference](pages/api-reference.md)** - Library and core API docs
- **[Development Guide](pages/development.md)** - Create new modules
- **[Full README](https://github.com/NatBuilds/TerminalOS/blob/main/README.md)** - Complete documentation

## 📋 Current Modules

| Module | Description |
|--------|-------------|
| **Settings** | Toggle verbose mode and view configuration |
| **Tools** | Example submenu structure and utilities |
| **Device Tools** | ADB utilities for Android device control |
| **Screenshot Analyzer** | ADB + OpenCV + Tesseract integrated example |
| **Cron Scheduler** | Task scheduling and automation interface |
| **Logs** | Application log management and search |

## 🤖 Why TerminalOS?

Tired of:
- ❌ Monolithic CLI applications?
- ❌ Restarting to test code changes?
- ❌ Complex menu routing logic?
- ❌ Scattered configuration management?

**TerminalOS solves all of this.** Every module is independently discoverable, automatically loaded, and reloaded on code change. Your menu system is built at runtime. Your business logic lives in clean service layers.

## 🛠️ Built For

- **System Administrators** - Automation dashboards
- **Mobile Developers** - Android device automation workflows
- **DevOps Engineers** - Multi-tool CLI interfaces
- **Python Developers** - Modular feature development

## 📦 What's Included

```
TerminalOS/
├── app/
│   ├── core/              # Menu, UI, status, config
│   ├── libraries/         # ADB, OpenCV, OCR, logging, cron
│   └── modules/           # Auto-discovered features
├── docs/                  # GitHub Pages documentation
└── templates/             # Module scaffolding
```

## 🔧 Requirements

- **Python 3.12+**
- **Core**: `colorama`, `requests`
- **Optional**: `opencv-python` (image processing), `pytesseract` (OCR), Android SDK (ADB)

## 💡 Example: Create a New Feature in 30 Seconds

```python
# app/modules/myfeature/controller.py
from app.core import status

def my_action() -> None:
    status.success("Feature works!")

def register(menu) -> None:
    menu.add("My Feature", my_action)
```

Save and run `python run.py` - it's automatically in your menu! Change code and it reloads on next menu render.

## 📱 Android Integration

Control Android devices directly:

```python
from app.libraries import ADBController

adb = ADBController()
adb.screenshot("screen.png")
adb.tap(100, 200)
adb.talk("Hello Android")
adb.open_app("com.android.chrome")
```

## 📜 License

MIT License - See [LICENSE](https://github.com/NatBuilds/TerminalOS/blob/main/LICENSE)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](https://github.com/NatBuilds/TerminalOS/blob/main/CONTRIBUTING.md)

---

**[View on GitHub](https://github.com/NatBuilds/TerminalOS)** | **[Report an Issue](https://github.com/NatBuilds/TerminalOS/issues)** | **[Documentation](pages/quick-start.md)**

