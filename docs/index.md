# TerminalOS

> **A MODULAR AUTOMATION OS FOR YOUR TERMINAL**
>
> AUTOMATE • EXTEND • CONTROL

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-00d9ff)](LICENSE)

Build, run and automate anything from a single, reloadable CLI platform. TerminalOS is a production-ready backbone for modular Python applications with live code reloading, automatic module discovery, and comprehensive Android automation capabilities.

---

## ✨ Core Capabilities

<div class="features">

<div class="feature-box">

### 🤖 Android Automation
**ADB Control and UI Actions**

- Full Android device control
- Tap, swipe, text input
- Screenshot capture
- App management

</div>

<div class="feature-box">

### 📸 Screenshot Analysis
**Tesseract OCR + OpenCV**

- Advanced image processing
- Text extraction from screens
- Visual element detection
- Integrated analysis pipeline

</div>

<div class="feature-box">

### 🧠 AI Integration
**Local LLM Support**

- LM Studio integration
- Terminal-based AI interactions
- Context-aware automation
- No internet required

</div>

<div class="feature-box">

### ⏰ Cron Scheduler
**Schedule Tasks and Jobs**

- Cron-like syntax automation
- Background task execution
- Job monitoring
- Performance tracking

</div>

<div class="feature-box">

### 📋 Logging & Diagnostics
**Detailed Session Tracking**

- Automatic session logging
- Performance diagnostics
- Error tracking
- Success reporting

</div>

<div class="feature-box">

### 🔌 Dynamic Modules
**Auto-Discovered Features**

- Drop modules into folders
- Auto-load on startup
- Hot reload without restart
- Clean separation of concerns

</div>

</div>

---

## 🎯 Why TerminalOS?

### ✅ Drop New Modules. They Load Automatically.
```python
# app/modules/myfeature/controller.py
def my_handler() -> None:
    status.success("Working!")

def register(menu) -> None:
    menu.add("My Feature", my_handler)
```

### ✅ Edit Code. See Changes Instantly.
No restart needed. Change your module and select it again—changes appear live!

### ✅ Professional-Grade Architecture
- Clean layer separation (UI, config, business logic)
- Comprehensive error handling
- Automatic session logging
- Configuration management

### ✅ Android Automation Built-In
30+ methods for device control, screenshot capture, and interaction via ADB.

### ✅ Extensible By Design
Thin controllers, business logic in services, reusable libraries for common tasks.

---

## 🚀 Getting Started (5 minutes)

```bash
# Clone the repository
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # macOS/Linux

# Install and run
pip install -r requirements.txt
python run.py
```

### Build Your First Module

Create `app/modules/hello/controller.py`:

```python
from app.core import status

def greet() -> None:
    status.success("Hello, World!")

def register(menu) -> None:
    menu.add("Say Hello", greet)
```

Run and your feature appears in the menu! 🎉

---

## 📚 Documentation

| Guide | Time | Purpose |
|-------|------|---------|
| **[Quick Start](pages/quick-start.md)** | 5 min | Installation & first steps |
| **[Architecture](pages/architecture.md)** | 15 min | Technical deep-dive |
| **[API Reference](pages/api-reference.md)** | 30 min | 70+ methods documented |
| **[Development](pages/development.md)** | 20 min | Building features |

---

## 📦 Included Modules

| Module | Features |
|--------|----------|
| **Settings** | Configuration & verbose mode |
| **Tools** | UI patterns & utilities |
| **Device Tools** | Android automation (11+ options) |
| **Screenshot Analyzer** | ADB + OpenCV + Tesseract |
| **Cron Scheduler** | Task scheduling interface |
| **Logs** | Session management |

---

## 🛠️ Built-In Libraries

### Android Automation (30+ methods)
ADB controller for full device automation

### Image Processing (20+ methods)
OpenCV integration for vision tasks

### Text Extraction (8+ methods)
Tesseract OCR for screen reading

### File & Text Tools
File operations and string manipulation

### Task Scheduling
Cron-like background automation

### LLM Integration
Local AI support via LM Studio

---

## 💡 Use Cases

### 🏢 System Administrators
Automation dashboards and infrastructure control

### 📱 Mobile Developers
Android device automation and testing

### 🚀 DevOps Engineers
Multi-tool CLI interfaces and deployments

### 👨‍💻 Python Developers
Learn modular architecture patterns

---

## ✨ Why Developers Love TerminalOS

✨ **Zero Configuration** - Just drop modules in folders
✨ **Hot Reload** - Changes apply instantly without restart
✨ **Professional** - Production-ready with logging & error handling
✨ **Documented** - 100+ examples, 70+ API methods
✨ **Integrated** - Android, AI, OCR, Scheduling all built-in
✨ **Extensible** - Clean architecture for your own features

---

## 🌟 Key Statistics

- **5** integrated modules ready to use
- **30+** Android automation methods
- **70+** total API methods
- **100+** code examples in docs
- **15,000+** words of guides
- **0** dependencies for core features

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](https://github.com/NatBuilds/TerminalOS/blob/main/CONTRIBUTING.md)

---

## 📜 License

MIT License - Open source and free for everyone

---

## 🚀 Ready to Build?

**[Start the Quick Start Guide →](pages/quick-start.md)**

Or explore the [full documentation](pages/architecture.md)

---

**[GitHub](https://github.com/NatBuilds/TerminalOS)** | **[Issues](https://github.com/NatBuilds/TerminalOS/issues)** | **[Docs](pages/quick-start.md)**

*TerminalOS - Build modular CLI applications. Automate, Extend, Control.* ✨

