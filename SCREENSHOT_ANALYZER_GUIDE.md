# Screenshot Analysis Example Module

## Installation

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
pip install -r requirements.txt
python run.py
```

Then navigate to: **Device Tools → ADB Screenshot and read**

## Overview

The **Screenshot Analyzer** module (`app/modules/screenshot_analyzer/`) is a complete example demonstrating how to use all three libraries together in a real-world workflow:

1. **ADB Controller** - Capture device screenshots
2. **OpenCV** - Process and analyze images  
3. **Tesseract OCR** - Extract text from the screen

This module serves as both a practical tool and a learning resource for integrating multiple libraries.

## What It Does

The "ADB Screenshot and read" menu item performs the following workflow:

### 1. Device Connection
- Initializes ADB controller
- Verifies ADB is available
- Lists connected devices
- Targets the first device (or configured device)

### 2. Screenshot Capture
- Creates a `screenshots/` directory in the project root
- Executes screencap on the device
- Pulls the image to the local filesystem

### 3. Image Processing (OpenCV)
- Loads the screenshot
- Converts to grayscale (better for OCR)
- Creates blurred version (noise reduction)
- Performs edge detection (UI structure analysis)
- Saves all processed versions for inspection

### 4. Text Extraction (Tesseract OCR)
- Extracts all visible text from the screenshot
- Shows confidence scores for each detected text item
- Filters results (shows only >50% confidence items)
- Displays detailed analysis

### 5. Results Storage
All outputs are saved to `screenshots/`:
- `device_screenshot.png` - Original screenshot
- `processed_grayscale.png` - Grayscale version
- `processed_blurred.png` - Blurred version
- `processed_edges.png` - Edge detection

## How to Use

### Quick Start
```bash
python run.py
# Navigate to: "ADB Screenshot and read" menu
```

### In Your Own Code

Copy the pattern used in the module:

```python
from app.libraries.adb import ADBController
from app.libraries.opencv import OpenCVImageTools
from app.libraries.ocr import TesseractOCR
from app.core import status
from pathlib import Path

def my_screenshot_handler() -> None:
    # 1. ADB Screenshot
    adb = ADBController()
    if not adb.is_available():
        status.error("ADB not available")
        return
    
    screenshot_path = Path("screenshots/my_screenshot.png")
    if not adb.screenshot(str(screenshot_path)):
        status.error("Failed to capture screenshot")
        return
    
    # 2. OpenCV Processing
    cv = OpenCVImageTools()
    if cv.is_available():
        image = cv.load_image(str(screenshot_path))
        gray = cv.to_grayscale(image)
        edges = cv.detect_edges(image)
        # Process further...
    
    # 3. Tesseract OCR
    ocr = TesseractOCR()
    if ocr.is_available():
        text = ocr.extract_text(str(screenshot_path))
        status.success(f"Extracted text:\n{text}")
```

## Key Design Patterns

### 1. Availability Checking
Each library is optional. Always check before using:
```python
cv = OpenCVImageTools()
if not cv.is_available():
    status.warning("OpenCV not available")
```

### 2. Robust Error Handling
Return early on errors:
```python
image = cv.load_image(str(screenshot_path))
if image is None:
    status.error("Failed to load image")
    return
```

### 3. Config-Driven Initialization
Libraries load configuration automatically:
```python
# This reads from app/config.json [adb] section
adb = ADBController()

# Can override with explicit params
adb = ADBController(
    adb_executable="/custom/path/adb",
    device_serial="specific_device",
    timeout=60
)
```

### 4. Cross-Platform Paths
Use `pathlib.Path()` for filesystem operations:
```python
# Works on Windows, macOS, Linux
app_root = Path(__file__).resolve().parents[2]
output_dir = app_root / "screenshots"
output_dir.mkdir(parents=True, exist_ok=True)
```

### 5. Status Logging
Use the status module for all output (not print):
```python
from app.core import status

status.info("Processing...")
status.debug("Detailed debug info")  # Only shows if verbose is ON
status.warning("Warning message")
status.error("Error message")
status.success("Success!")
```

## Output Examples

When run, the module produces output like:

```
[OK] ADB is available
[OK] Found 1 device(s)
[INFO]   - X5BDU19115000764 [device]
[OK] Screenshot saved: C:\...\screenshots\device_screenshot.png
[INFO] OpenCV initialized
[INFO] Processing image with OpenCV...
[DEBUG] Saved grayscale version
[DEBUG] Saved blurred version
[DEBUG] Saved edge detection
[INFO] Image processing complete
[WARNING] Tesseract OCR not available. Skipping OCR.

=== Analysis Summary ===
[INFO] Screenshot: C:\...\screenshots\device_screenshot.png
[INFO] Processed Images:
[INFO]   - Grayscale: C:\...\screenshots\processed_grayscale.png
[INFO]   - Blurred: C:\...\screenshots\processed_blurred.png
[INFO]   - Edges: C:\...\screenshots\processed_edges.png
[INFO] All files saved to: C:\...\screenshots
```

## Extending the Example

### Add Batch Processing
```python
def batch_process_screenshots() -> None:
    """Process multiple screenshots in sequence"""
    for device in adb.devices():
        screenshot_path = screenshots_dir / f"{device.serial}.png"
        adb.screenshot(str(screenshot_path), serial=device.serial)
        # Process...
```

### Add Comparison
```python
def compare_screenshots() -> None:
    """Compare two screenshots for differences"""
    prev_image = cv.load_image("screenshots/previous.png")
    curr_image = cv.load_image("screenshots/current.png")
    
    # Compute difference
    diff = cv2.absdiff(prev_image, curr_image)
    # Analyze...
```

### Add OCR Language Support
```python
def extract_german_text() -> None:
    """Extract German text from screenshot"""
    ocr = TesseractOCR(language="deu")
    text = ocr.extract_text(screenshot_path, language="deu")
    status.success(text)
```

### Add UI Automation
```python
def automate_with_ocr() -> None:
    """Use OCR to find and tap buttons"""
    ocr = TesseractOCR()
    data = ocr.extract_data(screenshot_path)
    
    # Find button coordinates
    for text, left, top, width, height in zip_data(data):
        if "Login" in text:
            # Tap the button
            adb.tap(left + width//2, top + height//2)
```

## Configuration

### ADB Settings (`app/config.json`)
```json
{
  "adb": {
    "adb_executable": "adb",      // Path to adb binary
    "device_serial": "",           // Leave empty for auto-detect
    "timeout": 30                  // Command timeout in seconds
  }
}
```

### OCR Settings (`app/config.json`)
```json
{
  "ocr": {
    "tesseract_cmd": "tesseract",  // Path to tesseract binary
    "language": "eng",             // OCR language
    "psm": 3,                      // Page segmentation mode
    "oem": 3,                      // OCR engine mode
    "timeout": 30                  // OCR timeout in seconds
  }
}
```

## Troubleshooting

### "ADB is not available"
- Install Android SDK Platform Tools
- Add `adb` to system PATH
- Or set `adb_executable` in `app/config.json`

### "No ADB devices connected"
- Enable USB debugging on your Android device
- Connect device via USB
- Accept the ADB connection prompt on device
- Run `adb devices` to verify

### "OpenCV not available"
- Install: `pip install opencv-python`

### "Tesseract OCR not available"
- Install Tesseract system-wide:
  - **Windows**: `choco install tesseract` or use installer
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt-get install tesseract-ocr`
- Install Python wrapper: `pip install pytesseract`

### OCR returning no text
- Try different PSM modes (0-13) in config
- Try preprocessing with OpenCV (blur, threshold)
- Check image contrast and brightness

## Code Structure

```
app/modules/screenshot_analyzer/
├── __init__.py              # Package marker
└── controller.py            # Main module
    ├── adb_screenshot_and_read()    # Main handler
    ├── demo_adb_screenshot_menu()   # Menu wrapper
    └── register()                   # Module registration
```

## Learning Outcomes

By studying this module, you'll learn:

1. **Library Integration** - How to use multiple libraries together
2. **Configuration Management** - Reading from `app/config.json`
3. **Error Handling** - Graceful degradation when libraries unavailable
4. **File Operations** - Cross-platform path handling
5. **Module Structure** - Following the app conventions
6. **Status Logging** - Proper output formatting
7. **Workflow Patterns** - Real-world automation workflow

This module is designed to be both functional and educational!

