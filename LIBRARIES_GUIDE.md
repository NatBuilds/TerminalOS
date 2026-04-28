# Libraries Guide

Complete API reference for all TerminalOS libraries. All libraries are designed to be optional with graceful degradation when dependencies are unavailable.

## 1. ADB Controller (`app/libraries/adb`)

A comprehensive Android Debug Bridge controller for connecting to and controlling Android devices.

### Usage

```python
from app.libraries import ADBController, ADBDeviceInfo

adb = ADBController()

# Check availability
if not adb.is_available():
    print("ADB not found on PATH")

# List connected devices
devices = adb.devices()
for device in devices:
    print(f"{device.serial}: {device.state}")

# Execute shell commands
output = adb.shell("getprop ro.build.version.release")

# Input control
adb.talk("Hello World")          # Type text
adb.tap(100, 200)                # Tap coordinates
adb.press("KEYCODE_HOME")        # Press key
adb.hold("KEYCODE_POWER")        # Long press
adb.swipe(100, 100, 500, 500)    # Swipe

# App management
adb.open_app("com.example.app")
adb.is_app_running("com.example.app")
adb.install("/path/to/app.apk")
adb.uninstall("com.example.app")

# Device info
current_app = adb.current_foreground_app()
processes = adb.running_processes()

# Files
adb.push("/local/file", "/device/path")
adb.pull("/device/file", "/local/path")
adb.screenshot("/output/screenshot.png")

# Reboot
adb.reboot()
```

### Configuration

Edit `app/config.json` to customize ADB settings:

```json
{
  "adb": {
    "adb_executable": "adb",
    "device_serial": "",
    "timeout": 30
  }
}
```

## 2. OpenCV Image Tools (`app/libraries/opencv`)

Image processing and manipulation using OpenCV (requires `opencv-python`).

### Usage

```python
from app.libraries import OpenCVImageTools

tools = OpenCVImageTools()

if not tools.is_available():
    print("OpenCV not available")

# Load and save
image = tools.load_image("/path/to/image.png")
tools.save_image("/output/result.png", image)

# Basic operations
gray = tools.to_grayscale(image)
blurred = tools.blur(image, kernel_size=5)
edges = tools.detect_edges(image)

# Transformations
resized = tools.resize(image, width=640, height=480)
rotated = tools.rotate(image, angle=45)
cropped = tools.crop(image, left=10, top=10, width=100, height=100)

# Filtering
thresholded = tools.threshold(gray, threshold_value=127)
normalized = tools.normalize_brightness(gray)

# Annotations
tools.draw_text(image, "Label", position=(10, 30))
tools.draw_rectangle(image, (10, 10), (100, 100))
tools.draw_circle(image, (50, 50), radius=25)
tools.annotate_box(image, left=10, top=10, width=80, height=60, label="Object")

# Create blank canvas
blank = tools.create_blank(640, 480, color=(0, 255, 0))
```

### Requirements

Install OpenCV:
```bash
pip install opencv-python>=4.10.0.84
```

## 3. Tesseract OCR (`app/libraries/ocr`)

Optical Character Recognition using Tesseract (requires system installation and pytesseract).

### Usage

```python
from app.libraries import TesseractOCR

ocr = TesseractOCR()

if not ocr.is_available():
    print("Tesseract not available")

# Extract text from image
text = ocr.extract_text("/path/to/image.png")
print(text)

# Extract with specific language
text_de = ocr.extract_text("/path/to/image.png", language="deu")

# Extract detailed data (positions, confidence)
data = ocr.extract_data("/path/to/image.png")
print(data.get("text"))
print(data.get("conf"))

# Extract bounding boxes
boxes = ocr.extract_boxes("/path/to/image.png")

# Generate searchable PDF
pdf_bytes = ocr.extract_pdf("/path/to/image.png")
```

### Configuration

Edit `app/config.json` to customize OCR settings:

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

**PSM (Page Segmentation Mode)** modes:
- `0`: Orientation and script detection
- `3`: Fully automatic page segmentation (default)
- `6`: Assume single uniform block of text
- `11`: Sparse text

**OEM (OCR Engine Mode)**:
- `0`: Legacy engine only
- `1`: Neural nets LSTM engine only
- `2`: Legacy + LSTM
- `3`: Default (auto-select)

### Requirements

Install Tesseract system-wide:

**Windows**:
```bash
choco install tesseract
# or download installer from: https://github.com/UB-Mannheim/tesseract/wiki
```

**macOS**:
```bash
brew install tesseract
```

**Linux**:
```bash
sudo apt-get install tesseract-ocr
```

Then install Python wrapper:
```bash
pip install pytesseract>=0.3.13
```

## Accessing from Modules

All three libraries are accessible from any module:

```python
from app.libraries import ADBController, OpenCVImageTools, TesseractOCR
from app.core import status

def my_handler() -> None:
    adb = ADBController()
    cv = OpenCVImageTools()
    ocr = TesseractOCR()
    
    status.info(f"ADB available: {adb.is_available()}")
    status.info(f"OpenCV available: {cv.is_available()}")
    status.info(f"OCR available: {ocr.is_available()}")
```

## Device Tools Module

A new menu module `app/modules/device_tools/` provides interactive access to all three libraries via:

### ADB Utilities
- List connected devices
- Run shell commands
- Send text to device
- Tap screen
- Press/hold keys
- Swipe screen
- Open apps
- Check running apps
- Show running processes
- Show foreground app

### Vision Tools
- OpenCV image processing (grayscale, blur, edge detection)
- Tesseract OCR text extraction
- Tesseract OCR data output

Access these from the main menu after launching `python run.py`.

