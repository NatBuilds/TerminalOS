# API Reference

Complete reference for all TerminalOS libraries and core modules.

## Core Modules

### status.py - Centralized Logging

```python
from app.core import status

# Basic logging
status.info(message)        # Info level
status.warning(message)     # Warning level
status.error(message)       # Error level
status.success(message)     # Success level
status.debug(message)       # Debug (only if verbose enabled)
```

All messages are:
- Printed to console with colors
- Automatically logged to `logs/session_*.log`
- Included in session statistics

### config.py - Configuration Management

```python
from app.core import config

# Read configuration
verbose = config.get_verbose()
adb_timeout = config.get_adb_timeout()
device_serial = config.get_device_serial()
tesseract_cmd = config.get_tesseract_cmd()
adb_executable = config.get_adb_executable()

# Write configuration
config.toggle_verbose()
config.set_adb_timeout(60)
config.set_device_serial("device123")
config.set_tesseract_cmd("tesseract")
config.set_adb_executable("adb")

# Get raw config dict
full_config = config.get_config()
```

**Config File Structure** (`app/config.json`):
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

### menu.py - Menu System

```python
from app.core.menu import Menu

# Create menu
menu = Menu("Menu Title")

# Add items
menu.add("Option 1", handler_function)
menu.add("Option 2", handler_function)

# Show menu
menu.show()
```

Handlers must be **no-arg callables**:
```python
def my_handler() -> None:
    # Your code here
    pass

# Use function
menu.add("Label", my_handler)

# Or use lambda
menu.add("Label", lambda: my_handler())
```

### ui.py - Console Output

```python
from app.core import ui

ui.clear_screen()           # Clear terminal
ui.print_banner()           # Show ASCII art banner
ui.print_header(text)       # Print formatted header
```

## Libraries

### ADBController - Android Device Control

```python
from app.libraries import ADBController

adb = ADBController()

# Device Management
devices = adb.devices()                    # List connected devices
adb.set_device(serial)                     # Set target device
adb.is_available()                         # Check if ADB available
adb.get_device_info()                      # Get device details
adb.get_android_version()                  # Get Android version

# Interaction
adb.tap(x, y)                              # Tap coordinates
adb.swipe(x1, y1, x2, y2)                 # Swipe from to
adb.press(keycode)                         # Press key (HOME, BACK, etc)
adb.talk(text)                             # Type text input
adb.enter()                                # Press Enter

# App Management
adb.open_app(package_name)                 # Launch app
adb.close_app(package_name)                # Close app
adb.is_app_running(package_name)           # Check if running
adb.get_installed_apps()                   # List installed apps
adb.uninstall_app(package_name)            # Remove app

# Clipboard
adb.set_clipboard(text)                    # Copy to clipboard
adb.get_clipboard()                        # Read clipboard

# Files
adb.push(local_path, device_path)          # Copy to device
adb.pull(device_path, local_path)          # Copy from device
adb.screenshot(output_path)                # Capture screen
adb.screen_record(output_path, duration)   # Record video

# Shell Commands
adb.shell(command)                         # Execute shell command
adb.reboot()                               # Reboot device

# System Info
adb.get_battery_level()                    # Battery percentage
adb.is_screen_on()                         # Screen state
adb.get_display_resolution()               # Screen size
```

### OpenCVImageTools - Image Processing

```python
from app.libraries import OpenCVImageTools

cv = OpenCVImageTools()

# Loading/Saving
image = cv.load_image(path)                # Load image
cv.save_image(image, path)                 # Save image
cv.get_image_properties(image)             # Get dimensions/channels

# Color Operations
gray = cv.to_grayscale(image)              # Convert to grayscale
hsv = cv.to_hsv(image)                     # Convert to HSV
rgb = cv.to_rgb(image)                     # Convert to RGB
bgr = cv.to_bgr(image)                     # Convert to BGR

# Transformations
resized = cv.resize(image, width, height)  # Resize image
rotated = cv.rotate(image, angle)          # Rotate image
flipped_h = cv.flip_horizontal(image)      # Flip horizontally
flipped_v = cv.flip_vertical(image)        # Flip vertically

# Filters & Effects
blurred = cv.blur(image, kernel_size)      # Apply blur
sharp = cv.sharpen(image)                  # Sharpen image
edges = cv.canny_edges(image)              # Edge detection
dilated = cv.dilate(image, kernel_size)    # Dilate image
eroded = cv.erode(image, kernel_size)      # Erode image

# Thresholding
thresh = cv.threshold(image, value)        # Binary threshold
adaptive = cv.adaptive_threshold(image)    # Adaptive threshold

# Feature Detection
contours = cv.find_contours(image)         # Find shapes
circles = cv.find_circles(image)           # Detect circles
lines = cv.find_lines(image)               # Detect lines

# Histograms
hist = cv.histogram(image)                 # Compute histogram
equalized = cv.histogram_equalization(image)

# Template Matching
matches = cv.template_match(image, template)
```

### TesseractOCR - Text Extraction

```python
from app.libraries import TesseractOCR

ocr = TesseractOCR()

# Text Extraction
text = ocr.extract_text(image_path)        # Extract all text
text = ocr.extract_text_from_region(image_path, x, y, w, h)

# Configuration
ocr.set_language("eng")                    # Set OCR language
ocr.set_psm(3)                             # Set page segmentation mode
ocr.set_oem(3)                             # Set OCR engine mode

# Detailed Results
data = ocr.get_detailed_text(image_path)   # Returns confidence scores

# Image Preparation
processed = ocr.preprocess_image(image_path)  # Improve OCR accuracy
```

### FileTools - File Operations

```python
from app.libraries.files import FileTools

ft = FileTools()

# Reading
content = ft.read_file(path)               # Read entire file
lines = ft.read_lines(path)                # Read as lines
exists = ft.file_exists(path)              # Check if exists

# Writing
ft.write_file(path, content)               # Write content
ft.append_file(path, content)              # Append to file
ft.create_file(path)                       # Create empty file

# Directory Operations
ft.create_directory(path)                  # Create directory
ft.delete_file(path)                       # Delete file
ft.delete_directory(path)                  # Delete directory
files = ft.list_files(directory)           # List files
files = ft.list_files_recursive(directory) # List recursively

# File Info
size = ft.get_file_size(path)              # File size in bytes
modified = ft.get_modified_time(path)      # Last modified

# Backup & Copy
ft.backup_file(path)                       # Create backup
ft.copy_file(source, dest)                 # Copy file
```

### TextTools - Text Utilities

```python
from app.libraries.text import TextTools

text = TextTools()

# String Operations
upper = text.to_uppercase(string)          # Convert to upper
lower = text.to_lowercase(string)          # Convert to lower
reversed_s = text.reverse_string(string)   # Reverse string
count = text.count_words(string)           # Count words
count = text.count_chars(string)           # Count characters

# Validation
is_email = text.is_valid_email(string)     # Validate email
is_url = text.is_valid_url(string)         # Validate URL
is_json = text.is_valid_json(string)       # Validate JSON

# Formatting
trimmed = text.trim_whitespace(string)     # Remove whitespace
camel = text.to_camelcase(string)          # Convert to camelCase
snake = text.to_snakecase(string)          # Convert to snake_case
```

### CronScheduler - Task Scheduling

```python
from app.libraries.cron import CronScheduler

scheduler = CronScheduler()

# Add Task
scheduler.add_task(
    name="task_name",
    cron_expression="0 9 * * *",  # 9 AM daily
    handler=my_function,
    description="Task description"
)

# List Tasks
tasks = scheduler.list_tasks()

# Remove Task
scheduler.remove_task("task_name")

# Get Task Status
status = scheduler.get_task_status("task_name")

# Cron Expression Format
# ┌───────────── second (0-59)
# │ ┌───────────── minute (0 - 59)
# │ │ ┌───────────── hour (0 - 23)
# │ │ │ ┌───────────── day of month (1 - 31)
# │ │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
# │ │ │ │ │ │
# * * * * * *

# Examples:
# "0 9 * * *"       # 9 AM every day
# "0 */4 * * *"     # Every 4 hours
# "0 0 * * 0"       # Sunday at midnight
# "0 14 * * MON"    # 2 PM on Mondays
```

### LLMChat - Large Language Model Integration

```python
from app.libraries.llm import LLMChat

llm = LLMChat()

# Check Availability
available = llm.check_availability()

# Send Message
response = llm.send_message("Your prompt here")

# Configuration (in config.json)
# "llm": {
#   "provider": "lm_studio",
#   "base_url": "http://localhost:1234",
#   "model": "your-model-name",
#   "timeout": 30
# }
```

## Common Workflows

### Workflow: Capture and Analyze Screen

```python
from app.core import status
from app.libraries import ADBController, TesseractOCR, OpenCVImageTools

def analyze_screen() -> None:
    adb = ADBController()
    ocr = TesseractOCR()
    cv = OpenCVImageTools()
    
    # Capture screenshot
    adb.screenshot("screenshot.png")
    status.success("Screenshot captured")
    
    # Process image
    image = cv.load_image("screenshot.png")
    gray = cv.to_grayscale(image)
    cv.save_image(gray, "processed.png")
    
    # Extract text
    text = ocr.extract_text("processed.png")
    status.info(f"Extracted text: {text[:100]}")
    status.success("Analysis complete")
```

### Workflow: Schedule Task

```python
from app.core import status
from app.libraries.cron import CronScheduler

def my_scheduled_task() -> None:
    status.success("Task executed!")

def schedule_task() -> None:
    scheduler = CronScheduler()
    scheduler.add_task(
        name="my_task",
        cron_expression="0 9 * * *",  # 9 AM daily
        handler=my_scheduled_task,
        description="Daily scheduled task"
    )
    status.success("Task scheduled")

def register(menu) -> None:
    menu.add("Schedule Task", schedule_task)
```

### Workflow: File Operations

```python
from app.core import status
from app.libraries.files import FileTools

def process_files() -> None:
    ft = FileTools()
    
    # Read
    files = ft.list_files("input/")
    status.info(f"Found {len(files)} files")
    
    # Process
    for file in files:
        content = ft.read_file(file)
        processed = content.upper()
        ft.write_file(f"output/{file}", processed)
    
    status.success("Files processed")
```

## Error Handling

All library functions handle errors and report via status:

```python
from app.core import status
from app.libraries import ADBController

def safe_adb_operation() -> None:
    try:
        adb = ADBController()
        if not adb.is_available():
            status.error("ADB not available")
            return
        
        devices = adb.devices()
        status.success(f"Found {len(devices)} devices")
    
    except Exception as e:
        status.error(f"Operation failed: {e}")
```

---

**[← Architecture](architecture.md)** | **[Development Guide →](development.md)**

