# TerminalOS - Libraries & Modules Reference

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

## 🚀 Quick Links

### Getting Started
- **Start Here**: [QUICK_START.md](QUICK_START.md) - 5 minute quick start guide
- **Run It Now**: `python run.py` → Select "Device Tools" or "ADB Screenshot and read"

### Documentation
- [LIBRARIES_GUIDE.md](LIBRARIES_GUIDE.md) - Complete API reference for all three libraries
- [SCREENSHOT_ANALYZER_GUIDE.md](SCREENSHOT_ANALYZER_GUIDE.md) - Detailed walkthrough of the example module
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical overview and architecture

## 📚 Three New Libraries

### 1. ADB Controller
**Location**: `app/libraries/adb/adb_controller.py`

Control Android devices via ADB (Android Debug Bridge).

```python
from app.libraries import ADBController

adb = ADBController()
devices = adb.devices()
adb.tap(100, 200)
adb.talk("Hello")
output = adb.shell("getprop ro.build.version.release")
```

**Features**:
- 26 methods for device automation
- Device discovery and management
- Input control (tap, swipe, text, press, hold)
- App management
- File transfer (push, pull, screenshot)
- Shell command execution

### 2. OpenCV Image Tools
**Location**: `app/libraries/opencv/image_tools.py`

Image processing and computer vision operations.

```python
from app.libraries import OpenCVImageTools

cv = OpenCVImageTools()
image = cv.load_image("screenshot.png")
gray = cv.to_grayscale(image)
edges = cv.detect_edges(image)
cv.save_image("output.png", edges)
```

**Features**:
- 20 image processing methods
- Load/save images
- Color space conversions
- Filtering and blur
- Edge detection
- Geometric transforms
- Annotations

### 3. Tesseract OCR
**Location**: `app/libraries/ocr/tesseract_ocr.py`

Extract text from images using Tesseract OCR.

```python
from app.libraries import TesseractOCR

ocr = TesseractOCR()
text = ocr.extract_text("image.png")
data = ocr.extract_data("image.png")
```

**Features**:
- Text extraction with confidence scores
- Multi-language support
- Bounding box detection
- PDF generation
- Detailed OCR data extraction

## 🎯 Two New Modules

### Device Tools Module
**Location**: `app/modules/device_tools/`

Interactive menu with 14 device control options:

**ADB Utilities** (11 options):
- List devices
- Run shell commands
- Send text to device
- Tap screen
- Press/hold keys
- Swipe screen
- Open/check apps
- Show running processes

**Vision Tools** (3 options):
- OpenCV image processing
- Tesseract text extraction
- Tesseract data output

### Screenshot Analyzer Module
**Location**: `app/modules/screenshot_analyzer/`

Complete example showing all three libraries working together:

1. Captures device screenshot via ADB
2. Processes image with OpenCV (grayscale, blur, edges)
3. Extracts text with Tesseract OCR
4. Saves all outputs to `screenshots/` directory
5. Displays comprehensive analysis results

**280+ lines with detailed comments explaining each step and design decisions.**

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Install Python dependencies (already done)
pip install -r requirements.txt

# ADB (Android Debug Bridge)
# Windows: choco install android-sdk
# macOS: brew install android-platform-tools
# Linux: sudo apt-get install android-tools-adb

# Tesseract OCR (Optional)
# Windows: choco install tesseract
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

### Connect Android Device
1. Enable USB debugging on your Android device
2. Connect via USB
3. Accept the ADB connection prompt
4. Run `adb devices` to verify

## 💻 Usage Examples

### Example 1: List Devices
```python
from app.libraries import ADBController

adb = ADBController()
for device in adb.devices():
    print(f"{device.serial}: {device.state}")
```

### Example 2: Capture & Process Screenshot
```python
from app.libraries import ADBController, OpenCVImageTools
from pathlib import Path

adb = ADBController()
cv = OpenCVImageTools()

# Capture
path = Path("screenshot.png")
adb.screenshot(str(path))

# Process
image = cv.load_image(str(path))
edges = cv.detect_edges(image)
cv.save_image("edges.png", edges)
```

### Example 3: Full Workflow
See: `app/modules/screenshot_analyzer/controller.py` (280+ lines with comments)

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| [QUICK_START.md](QUICK_START.md) | Get started in 5 minutes |
| [LIBRARIES_GUIDE.md](LIBRARIES_GUIDE.md) | Complete API reference |
| [SCREENSHOT_ANALYZER_GUIDE.md](SCREENSHOT_ANALYZER_GUIDE.md) | Example walkthrough |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Technical overview |

## 🎮 How to Run

### Interactive Menu
```bash
python run.py

# Then select:
# - "Device Tools" for interactive device control
# - "ADB Screenshot and read" for complete example
```

### Programmatic Usage
```python
from app.libraries import ADBController, OpenCVImageTools, TesseractOCR
from app.core import status

# All libraries are directly importable
adb = ADBController()
cv = OpenCVImageTools()
ocr = TesseractOCR()

# Check availability
if adb.is_available():
    status.info("ADB is available")
```

## 📁 File Structure

```
app/
├── libraries/
│   ├── adb/
│   │   ├── __init__.py
│   │   └── adb_controller.py (370+ lines)
│   ├── opencv/
│   │   ├── __init__.py
│   │   └── image_tools.py (280+ lines)
│   ├── ocr/
│   │   ├── __init__.py
│   │   └── tesseract_ocr.py (160+ lines)
│   └── __init__.py (re-exports all classes)
├── modules/
│   ├── device_tools/
│   │   ├── __init__.py
│   │   └── controller.py (14 menu options)
│   └── screenshot_analyzer/
│       ├── __init__.py
│       └── controller.py (280+ lines with comments)
├── config.json (extended with adb & ocr sections)
└── core/
    └── config.py (extended with new getters)
```

## ✨ Key Features

### Graceful Degradation
Each library handles missing dependencies gracefully:
```python
cv = OpenCVImageTools()
if not cv.is_available():
    print("OpenCV not available")
```

### Configuration-Driven
All settings read from `app/config.json` with sensible defaults:
```json
{
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
  }
}
```

### Extensive Code Comments
Every implementation includes detailed comments explaining:
- What each section does
- Why it's done that way
- How to customize it

## 🔧 Troubleshooting

### "ADB is not available"
- Install Android SDK Platform Tools
- Add `adb` to system PATH
- Or configure in `app/config.json`

### "No devices found"
- Enable USB debugging on Android device
- Connect via USB
- Accept ADB connection prompt

### "OpenCV not available"
- Run: `pip install opencv-python`

### "Tesseract not available"
- Install system-wide (choco/brew/apt)
- Or configure path in `app/config.json`

## 🚀 Next Steps

1. **Try It Out**: Run `python run.py` and explore the menus
2. **Read the Docs**: Start with [QUICK_START.md](QUICK_START.md)
3. **Study the Example**: Check [SCREENSHOT_ANALYZER_GUIDE.md](SCREENSHOT_ANALYZER_GUIDE.md)
4. **Build Your Own**: Create custom modules using the pattern shown

## 📊 Statistics

- **Total Lines of Code**: 800+ lines of implementation
- **Total Methods**: 54+ public methods across three libraries
- **Documentation**: 1000+ lines of guides and comments
- **Example Module**: 280+ lines with detailed comments
- **Test Coverage**: All components tested with real device

## ✅ Validation

All components have been tested:
- ✓ Syntax validation
- ✓ Import validation
- ✓ Runtime instantiation
- ✓ Module discovery
- ✓ Menu integration
- ✓ Real device detection
- ✓ Screenshot capture
- ✓ Image processing

## 🎓 Learning Resources

This implementation serves as both a functional tool and a learning resource. Study how:
- Multiple libraries are integrated
- Configuration is managed
- Graceful degradation works
- Modules are structured
- Code is documented
- Error handling is done

Start with [SCREENSHOT_ANALYZER_GUIDE.md](SCREENSHOT_ANALYZER_GUIDE.md) for a complete learning walkthrough.

---

**Ready to explore?** Run `python run.py` and navigate to the new menu items!

