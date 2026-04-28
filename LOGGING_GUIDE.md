# Logging System Guide

## Installation & Setup

This logging system is built-in to TerminalOS and requires no additional setup:

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
pip install -r requirements.txt
python run.py
```

## Overview

A comprehensive file-based logging system automatically captures all application activity. All messages (info, warnings, errors, success, debug) are logged to timestamped files in the `logs/` directory.

Session logs are created automatically when the application starts, one per session.

## Features

### Automatic Logging
- Every status message is automatically logged to file
- Timestamped entries for easy tracking
- Session-based log files (one file per application session)
- Graceful handling of logging errors (doesn't break the app)

### Log Management
- Dedicated **Logs** menu module for viewing and managing logs
- Search functionality to find specific messages
- Error/warning summary views
- Session statistics tracking
- Automatic cleanup of old logs (>30 days)

## Session Information

- Session start time
- Total duration
- Message counts (total, errors, warnings)
- Log file location

## Location

All logs are stored in: `{project_root}/logs/`

Each session creates a file named: `session_YYYYMMDD_HHMMSS.log`

Example: `session_20260428_110735.log`

## Usage

### View Logs from CLI

Run the application and navigate to: **Logs**

Options available:
1. **View current session logs** - Show all messages from this session
2. **View session statistics** - Timing and message counts
3. **View error summary** - All errors and warnings
4. **Search logs** - Find specific messages
5. **View all log files** - List all session logs
6. **Show logs directory** - Display logs folder location
7. **Clear old logs** - Delete logs older than 30 days

### Programmatic Access

```python
from app.libraries.logging import get_logger, log_info, log_error

# Log a message
log_info("Application started")
log_error("Something failed")

# Get logger instance
logger = get_logger()
print(f"Messages logged: {logger.message_count}")
print(f"Errors: {logger.error_count}")
```

## Integration

### Automatic Status Logging

All status messages are automatically logged:

```python
from app.core import status

status.info("This gets logged")
status.error("Errors are logged")
status.warning("Warnings are logged")
status.success("Success messages are logged")
status.debug("Debug messages are logged (if verbose enabled)")
```

### Manual Logging

```python
from app.libraries.logging import log_info, log_error, log_warning, log_success

log_info("Custom message")
log_error("Error with context", error_code="E001", severity="high")
```

### Session Summary

Session summary is automatically written when the app exits:

```
================================================================================
Session Summary
================================================================================
Total Messages:  127
Errors:          3
Warnings:        8
Duration:        45.3 seconds
End Time:        2026-04-28 11:12:00
================================================================================
```

## Log File Format

Each log file contains:

```
================================================================================
TerminalOS Session Log
Started: 2026-04-28 11:11:15
================================================================================

11:11:16.234 [INFO] Application started
11:11:17.101 [SUCCESS] Connected to device
11:11:18.502 [DEBUG] Executing command: adb shell
11:11:19.003 [ERROR] Failed to capture screenshot
...
```

### Message Format

```
HH:MM:SS.mmm [LEVEL] Message text
```

- **HH:MM:SS.mmm** - Time with millisecond precision
- **[LEVEL]** - Message level: INFO, WARNING, ERROR, SUCCESS, DEBUG
- **Message text** - The actual message

### Extra Context

Important messages may include additional context:

```
11:11:19.003 [ERROR] Failed to capture screenshot
    error_code: E001
    device: X5BDU19115000764
    reason: file_not_created
```

## Storage & Cleanup

### Default Retention
- Logs are kept indefinitely by default
- Old logs are not deleted automatically

### Manual Cleanup
Use the **Logs** menu → **Clear old logs** to delete logs older than 30 days

Or programmatically:
```python
import time
from pathlib import Path

cutoff_time = time.time() - (30 * 24 * 60 * 60)  # 30 days ago
for log_file in Path("logs").glob("*.log"):
    if log_file.stat().st_mtime < cutoff_time:
        log_file.unlink()
```

## Statistics

Track session performance:

```python
from app.libraries.logging import get_stats

stats = get_stats()
print(f"Total messages: {stats['total_messages']}")
print(f"Errors: {stats['errors']}")
print(f"Warnings: {stats['warnings']}")
print(f"Duration: {stats['elapsed_seconds']} seconds")
```

## Troubleshooting

### Logs Not Being Created

1. Check directory permissions: `logs/` should be writable
2. Check disk space: ensure enough space for log files
3. Verify logging module is imported

### Logs Growing Too Large

- Use menu option **Clear old logs** regularly
- Or manually delete `logs/*.log` files

### Performance Impact

Logging is designed to be minimal overhead:
- Errors don't interrupt normal operation
- Logging happens on same thread (non-blocking)
- File writes are buffered

## Examples

### Example 1: View Recent Errors

```
Main Menu → Logs → View error summary
```

Shows all errors from the current session with timestamps.

### Example 2: Search for a Device Serial

```
Main Menu → Logs → Search logs
Enter search term: X5BDU19115000764
```

Finds all messages mentioning the specific device.

### Example 3: Get Session Performance

```
Main Menu → Logs → View session statistics
```

Displays timing information and message counts.

## Advanced Usage

### Custom Logging from Modules

```python
from app.libraries.logging import log_info, log_error

def my_feature():
    log_info("Feature started", feature="my_feature")
    try:
        # Do something
        log_info("Feature completed successfully")
    except Exception as exc:
        log_error(f"Feature failed: {exc}", feature="my_feature", traceback=str(exc))
```

### Reading Logs Programmatically

```python
from pathlib import Path

log_file = Path("logs/session_20260428_110735.log")
with open(log_file, "r") as f:
    for line in f:
        if "[ERROR]" in line:
            print(f"Error: {line.rstrip()}")
```

### Analyzing Log Patterns

```python
from collections import Counter
from pathlib import Path

log_dir = Path("logs")
error_counts = Counter()

for log_file in log_dir.glob("*.log"):
    with open(log_file, "r") as f:
        for line in f:
            if "[ERROR]" in line:
                error_counts[log_file.name] += 1

for session, count in error_counts.most_common():
    print(f"{session}: {count} errors")
```

## Integration Points

### Core Status Module
- `app/core/status.py` - All messages automatically logged

### Application Lifecycle
- `app/main.py` - Session summary written on exit

### Logging Library
- `app/libraries/logging/` - Core logging functionality

### Logs Module
- `app/modules/logs/` - Interactive menu for log management

## Performance Considerations

- **File I/O**: Logs are written synchronously (could add buffering in future)
- **Disk Space**: Monitor `logs/` directory size
- **Session Duration**: Longer sessions = larger log files

## Best Practices

1. **Use appropriate log levels**
   - `INFO` for normal operations
   - `WARNING` for recoverable issues
   - `ERROR` for failures
   - `DEBUG` for diagnostic information

2. **Include context** when logging errors
   - Device serial number
   - Operation being performed
   - Relevant parameters

3. **Review logs regularly** for patterns and issues

4. **Clean up old logs** periodically to save disk space

5. **Use search** to quickly find specific issues

## Summary

The logging system provides comprehensive tracking of all application activity. Use the **Logs** menu to view, search, and manage logs efficiently. All status messages are captured automatically for later review and troubleshooting.

