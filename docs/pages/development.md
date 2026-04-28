# Development Guide

Learn how to build advanced features for TerminalOS.

## Module Development Workflow

### 1. Create Module Structure

Create the directory and file:
```bash
mkdir app/modules/mymodule
touch app/modules/mymodule/controller.py
touch app/modules/mymodule/__init__.py
```

### 2. Implement register() Function

Every module needs a `register(menu)` function:

```python
# app/modules/mymodule/controller.py
from app.core import status

def my_action() -> None:
    status.success("Action executed!")

def register(menu) -> None:
    """Called automatically by TerminalOS"""
    menu.add("My Action", my_action)
```

### 3. Test Immediately

1. Run `python run.py`
2. Select your module from the main menu
3. Changes appear automatically on next menu render
4. Edit code and select again to test

## Separating Business Logic

Keep controllers thin by using a service module:

**app/modules/mymodule/controller.py:**
```python
from app.core import status
from .service import process_user_data

def handle_input() -> None:
    user_input = "some data"
    result = process_user_data(user_input)
    status.success(f"Result: {result}")

def register(menu) -> None:
    menu.add("Process Data", handle_input)
```

**app/modules/mymodule/service.py:**
```python
def process_user_data(data):
    """Complex business logic"""
    # Heavy processing, calculations, etc
    return processed_result

def validate_data(data):
    """Input validation"""
    return len(data) > 0

def format_output(result):
    """Output formatting"""
    return str(result)
```

## Working with Configuration

### Reading Configuration

```python
from app.core import config, status

def show_config() -> None:
    verbose = config.get_verbose()
    timeout = config.get_adb_timeout()
    
    status.info(f"Verbose: {verbose}")
    status.info(f"Timeout: {timeout}s")
```

### Modifying Configuration

```python
from app.core import config, status

def toggle_debug() -> None:
    config.toggle_verbose()
    verbose = config.get_verbose()
    status.success(f"Verbose mode: {verbose}")
```

### Creating Custom Config Keys

The config system is flexible. Add custom keys to `app/config.json`:

```json
{
  "verbose": false,
  "my_feature": {
    "enabled": true,
    "settings": "value"
  }
}
```

Then read with:
```python
from app.core import config

full_config = config.get_config()
my_settings = full_config.get("my_feature", {})
```

## Creating Submenus

Nested menus provide organization:

```python
from app.core import menu as menu_module, status

def sub_option_1() -> None:
    status.success("Sub-option 1 executed")

def sub_option_2() -> None:
    status.success("Sub-option 2 executed")

def show_submenu() -> None:
    submenu = menu_module.Menu("Sub-Menu Title")
    submenu.add("Sub-option 1", sub_option_1)
    submenu.add("Sub-option 2", sub_option_2)
    submenu.show()

def register(menu) -> None:
    menu.add("Open Submenu", show_submenu)
```

## Using Libraries

### Android Device Automation

```python
from app.core import status
from app.libraries import ADBController

def automate_device() -> None:
    adb = ADBController()
    
    # Check availability
    if not adb.is_available():
        status.error("ADB not available - install Android SDK")
        return
    
    # Get devices
    devices = adb.devices()
    if not devices:
        status.error("No Android devices connected")
        return
    
    # Use first device
    device = devices[0]
    adb.set_device(device.serial)
    
    # Perform actions
    adb.screenshot("screen.png")
    adb.tap(100, 200)
    adb.talk("Hello")
    
    status.success(f"Automated device: {device.serial}")

def register(menu) -> None:
    menu.add("Automate Device", automate_device)
```

### Image Processing

```python
from app.core import status
from app.libraries import OpenCVImageTools

def process_image() -> None:
    cv = OpenCVImageTools()
    
    # Load image
    image = cv.load_image("input.png")
    if image is None:
        status.error("Failed to load image")
        return
    
    # Process
    gray = cv.to_grayscale(image)
    edges = cv.canny_edges(gray)
    blurred = cv.blur(edges, 5)
    
    # Save result
    cv.save_image(blurred, "output.png")
    status.success("Image processed and saved")

def register(menu) -> None:
    menu.add("Process Image", process_image)
```

### Text Recognition (OCR)

```python
from app.core import status
from app.libraries import TesseractOCR

def extract_text() -> None:
    ocr = TesseractOCR()
    
    # Configure
    ocr.set_language("eng")
    
    # Extract text
    text = ocr.extract_text("screenshot.png")
    if not text:
        status.warning("No text found in image")
        return
    
    status.success(f"Extracted {len(text)} characters")
    status.info(f"Text: {text[:100]}...")

def register(menu) -> None:
    menu.add("Extract Text", extract_text)
```

### File Operations

```python
from app.core import status
from app.libraries.files import FileTools

def backup_files() -> None:
    ft = FileTools()
    
    # Create backup
    files = ft.list_files("data/")
    for file in files:
        ft.backup_file(file)
    
    status.success(f"Backed up {len(files)} files")

def register(menu) -> None:
    menu.add("Backup Files", backup_files)
```

## Error Handling Best Practices

### Try-Except with Status Reporting

```python
from app.core import status
import traceback

def safe_operation() -> None:
    try:
        # Your code here
        result = risky_operation()
        status.success(f"Success: {result}")
    
    except FileNotFoundError as e:
        status.error(f"File not found: {e}")
    except ValueError as e:
        status.error(f"Invalid value: {e}")
    except Exception as e:
        status.error(f"Unexpected error: {e}")
        # Debug info in verbose mode
        if config.get_verbose():
            status.debug(traceback.format_exc())
```

### Graceful Degradation

```python
from app.core import status
from app.libraries import ADBController

def optional_adb_feature() -> None:
    adb = ADBController()
    
    # Check if available, continue without it
    if adb.is_available():
        devices = adb.devices()
        status.info(f"Found {len(devices)} devices")
    else:
        status.warning("ADB not available, continuing without device control")
    
    # Rest of logic continues...
```

## Logging for Debugging

### Using Status for Logging

All `status.*` calls are automatically logged:

```python
from app.core import status

def debug_feature() -> None:
    status.debug("Debug message")     # Only if verbose enabled
    status.info("Info message")       # Always logged
    status.warning("Warning")         # Always logged
    status.error("Error")             # Always logged
    status.success("Success")         # Always logged
```

### Enable Verbose Mode

1. Run `python run.py`
2. Navigate to **Settings**
3. Toggle **Verbose Mode**
4. See debug output for your features

### Check Session Logs

```bash
# View latest session log
type logs\session_YYYYMMDD_HHMMSS.log

# See what happened during execution
# Format: [TIMESTAMP] [LEVEL] message
```

## Advanced Patterns

### Multi-Step Workflow

```python
from app.core import status

def step_one() -> None:
    status.info("Step 1: Processing...")
    status.success("Step 1 complete")

def step_two() -> None:
    status.info("Step 2: Analyzing...")
    status.success("Step 2 complete")

def step_three() -> None:
    status.info("Step 3: Reporting...")
    status.success("Step 3 complete")

def run_workflow() -> None:
    step_one()
    step_two()
    step_three()
    status.success("Workflow complete!")

def register(menu) -> None:
    menu.add("Run Workflow", run_workflow)
```

### Conditional Actions

```python
from app.core import status, config

def conditional_action() -> None:
    if config.get_verbose():
        status.debug("Extra debug info...")
    
    status.info("Main action running")
    status.success("Done")

def register(menu) -> None:
    menu.add("Conditional Action", conditional_action)
```

### Data Persistence

Use config or files for persistent data:

```python
from app.core import status, config
from app.libraries.files import FileTools

def save_data() -> None:
    ft = FileTools()
    
    data = {
        "timestamp": "2026-04-28",
        "status": "completed"
    }
    
    # Save as file
    import json
    ft.write_file("data.json", json.dumps(data))
    status.success("Data saved")

def load_data() -> None:
    ft = FileTools()
    import json
    
    content = ft.read_file("data.json")
    data = json.loads(content)
    status.info(f"Loaded: {data}")

def register(menu) -> None:
    menu.add("Save Data", save_data)
    menu.add("Load Data", load_data)
```

## Testing Your Module

### Manual Testing

1. Create/edit your module
2. Run `python run.py`
3. Navigate to your feature
4. Verify output in console
5. Check `logs/` for detailed logs

### Debug with Verbose Mode

1. Enable Verbose in Settings
2. Run your feature
3. Check for debug output
4. Review `logs/session_*.log` for full trace

### Edge Cases to Test

- Invalid input
- Missing files/devices
- Network issues (if applicable)
- Empty results
- Large data sets

## Common Mistakes to Avoid

❌ **Don't forget no-arg handlers:**
```python
# Wrong
menu.add("Action", my_handler("arg"))

# Right
menu.add("Action", my_handler)
```

❌ **Don't print directly:**
```python
# Wrong
print("Result:", result)

# Right
status.success(f"Result: {result}")
```

❌ **Don't use infinite loops:**
```python
# Wrong
def handler() -> None:
    while True:
        do_something()

# Right - return to menu
def handler() -> None:
    do_something()
    status.success("Done")
```

❌ **Don't crash without error reporting:**
```python
# Wrong
def handler() -> None:
    result = risky_operation()  # Can crash

# Right
def handler() -> None:
    try:
        result = risky_operation()
    except Exception as e:
        status.error(f"Failed: {e}")
```

## Publishing Your Module

1. Test thoroughly with manual testing
2. Enable verbose mode and check logs
3. Test error cases
4. Submit PR with:
   - New module folder with `controller.py`
   - Updated `README.md` with feature description
   - Example usage in docstring

---

**[← API Reference](api-reference.md)** | **[Back to Home](/)**

