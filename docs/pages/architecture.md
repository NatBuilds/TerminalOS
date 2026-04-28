# Architecture Guide

Deep dive into TerminalOS module system and design patterns.

## Core Principles

1. **Modular** - Each feature is self-contained in `app/modules/*/controller.py`
2. **Discoverable** - Modules are found and loaded automatically at runtime
3. **Reloadable** - Code changes are picked up on next menu render
4. **Clean** - Separate UI, status, config, and business logic
5. **Extensible** - Shared libraries for common tasks

## Layer Architecture

### Presentation Layer (`app/core/`)

**menu.py** - Menu system
- `Menu` class with `add(label, handler)` method
- Handlers must be no-arg callables
- Supports nested submenus
- Renders to terminal with user input

**ui.py** - Console output
- `print_banner()` - Display ASCII art
- `clear_screen()` - Clear terminal
- `print_header()` - Format section headers
- Safe formatting for Windows/Unix

**status.py** - Centralized logging
```python
from app.core import status

status.info("Informational message")
status.warning("Warning message")
status.error("Error message")
status.success("Success message")
status.debug("Debug message")  # Only if verbose enabled
```

All status calls are automatically logged to `logs/session_YYYYMMDD_HHMMSS.log`.

### Configuration Layer (`app/core/`)

**config.py** - Configuration management
```python
from app.core import config

# Read
verbose = config.get_verbose()
adb_timeout = config.get_adb_timeout()

# Write
config.toggle_verbose()
config.set_adb_timeout(60)
```

**Features:**
- Auto-creates `app/config.json` with defaults
- Auto-repairs invalid JSON
- Adds missing keys on startup
- Hot-reloadable during runtime

**cron_runtime.py** - Scheduled task execution
- Runs scheduled tasks at configured intervals
- Integrates with task scheduler library

### Business Logic Layers

**Module Controllers** (`app/modules/*/controller.py`)
- Entry point for each module
- Implements `register(menu) -> None`
- Adds menu items via `menu.add("Label", handler)`
- Handlers are no-arg callables

**Module Services** (`app/modules/*/service.py` - Optional)
- Contains business logic
- Imported by controller
- Keeps controllers thin

**Libraries** (`app/libraries/*/`)
- Shared utilities and integrations
- 30+ ADB methods, 20+ OpenCV methods, 8+ OCR methods
- All include error handling and status logging

## Module Discovery Contract

Every module must have:

1. **Location**: `app/modules/<name>/controller.py`
2. **Export**: A `register(menu) -> None` function
3. **Registration**: Add menu items via `menu.add(label, handler)`
4. **Handlers**: No-arg callables (functions or lambdas)

**Minimal Example:**

```python
from app.core import status

def my_handler() -> None:
    status.success("Handler executed!")

def register(menu) -> None:
    menu.add("My Menu Item", my_handler)
```

**How it works:**
```
1. app/main.py scans app/modules/ for subdirectories
2. Imports app/modules/<name>/controller.py
3. Calls register(menu) function
4. Module adds its items to menu
5. Menu displayed to user
6. User selects item → handler executes
7. Loop repeats, modules reloaded → live editing!
```

## Common Patterns

### Simple Action

```python
from app.core import status

def do_something() -> None:
    status.info("Starting...")
    # Business logic
    status.success("Done!")

def register(menu) -> None:
    menu.add("Do Something", do_something)
```

### Submenu

```python
from app.core import menu as menu_module

def show_submenu() -> None:
    submenu = menu_module.Menu("Sub-Options")
    submenu.add("Option 1", handler_one)
    submenu.add("Option 2", handler_two)
    submenu.show()

def register(menu) -> None:
    menu.add("Open Submenu", show_submenu)
```

### With Service Layer

**controller.py:**
```python
from app.core import status
from .service import process_data

def handle_processing() -> None:
    result = process_data(input_value)
    status.success(f"Result: {result}")

def register(menu) -> None:
    menu.add("Process", handle_processing)
```

**service.py:**
```python
def process_data(data):
    # Complex business logic
    return result
```

### Using Libraries

```python
from app.core import status
from app.libraries import ADBController

def device_action() -> None:
    adb = ADBController()
    if not adb.is_available():
        status.error("ADB not available")
        return
    
    devices = adb.devices()
    status.success(f"Found {len(devices)} devices")

def register(menu) -> None:
    menu.add("List Devices", device_action)
```

### Configuration Access

```python
from app.core import status, config

def check_settings() -> None:
    verbose = config.get_verbose()
    timeout = config.get_adb_timeout()
    status.info(f"Verbose: {verbose}, Timeout: {timeout}")

def register(menu) -> None:
    menu.add("Check Settings", check_settings)
```

## File Structure

```
app/
├── main.py                      # Runtime loop
├── config.json                  # Auto-created config
├── core/
│   ├── __init__.py
│   ├── menu.py                  # Menu system
│   ├── ui.py                    # Terminal rendering
│   ├── status.py                # Logging
│   ├── config.py                # Configuration
│   ├── cron_runtime.py          # Task scheduler
│   └── art.py                   # ASCII art
├── libraries/
│   ├── adb/adb_controller.py        # Android automation
│   ├── opencv/image_tools.py        # Image processing
│   ├── ocr/tesseract_ocr.py         # Text extraction
│   ├── logging/file_logger.py       # File logging
│   ├── cron/                        # Task scheduling
│   ├── files/file_tools.py          # File operations
│   ├── text/text_tools.py           # Text utilities
│   └── llm/llm_chat.py              # LLM integration
└── modules/                         # Auto-discovered
    ├── example/controller.py
    ├── settings/controller.py
    ├── tools/controller.py
    ├── device_tools/controller.py
    ├── screenshot_analyzer/controller.py
    ├── cron_scheduler/controller.py
    └── logs/controller.py
```

## Runtime Flow

```
1. User runs: python run.py
                    ↓
2. Imports app.main.main()
                    ↓
3. Scans app/modules/ for subdirectories
                    ↓
4. Imports each app/modules/<name>/controller.py
                    ↓
5. Creates Menu object
                    ↓
6. Calls each module's register(menu) function
   (modules add their items)
                    ↓
7. Renders menu to terminal
                    ↓
8. User selects item
                    ↓
9. Handler function executes (no-arg callable)
                    ↓
10. Back to step 3 (modules reloaded!)
                    ↓
    → This enables live code editing!
```

## Best Practices

### Do's

✅ Keep controllers thin - move logic to service.py  
✅ Use `status.success/warning/error` for user feedback  
✅ Catch exceptions in handlers and report via status  
✅ Test features by running relevant menu path  
✅ Use config for user preferences  
✅ Enable verbose mode for debugging  

### Don'ts

❌ Don't use infinite loops in handlers - return to menu  
❌ Don't hardcode credentials - use config.json  
❌ Don't print directly - use status module  
❌ Don't leave exceptions unhandled  
❌ Don't create global state that persists between reloads  
❌ Don't require app restart for feature changes  

## Error Handling

Always wrap handler logic:

```python
from app.core import status

def safe_handler() -> None:
    try:
        # Business logic
        status.success("Operation succeeded")
    except FileNotFoundError as e:
        status.error(f"File not found: {e}")
    except Exception as e:
        status.error(f"Unexpected error: {e}")
        if config.get_verbose():
            status.debug(f"Traceback: {traceback.format_exc()}")

def register(menu) -> None:
    menu.add("Safe Action", safe_handler)
```

## Testing Your Module

1. Create `app/modules/mymodule/controller.py`
2. Run `python run.py`
3. Navigate to your module
4. Edit code while app is running
5. Select menu item again to test changes
6. Check `logs/` for detailed output

Enable verbose mode in Settings for additional debug information.

## Available Libraries

### ADB Controller
30+ methods for Android device automation. See [API Reference](api-reference.md).

### OpenCV Image Tools
20+ methods for image processing and analysis.

### Tesseract OCR
8+ methods for text extraction from images.

### File Operations
Read/write/backup file operations with error handling.

### Text Utilities
String manipulation, formatting, and parsing utilities.

### Cron Scheduler
Task scheduling with cron-like syntax.

### Logging System
Automatic session logging with statistics.

---

**[← Quick Start](quick-start.md)** | **[API Reference →](api-reference.md)**

