# Cron Scheduler Guide

## Installation

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
pip install -r requirements.txt
python run.py
```

## Accessing the Scheduler

From the main menu, select **Cron Scheduler** to access all scheduling features.

## Overview

The Cron Scheduler is a modular task scheduling system that allows users to:
- Create, view, edit, and delete scheduled tasks
- Define execution times using standard cron expressions
- Execute predefined or custom task handlers at scheduled times
- Tasks persist between application sessions
- Background task execution with automatic checking

## Quick Start

1. **Run the application**:
   ```bash
   python run.py
   ```

2. **Access the Cron Scheduler module** from the main menu

3. **Create a new task**:
   - Choose "Create New Task"
   - Enter a task name (e.g., "Daily Report")
   - Enter a cron expression (e.g., "0 9 * * *" for 9 AM daily)
   - Select or enter a command to execute

## Cron Expression Format

Standard cron format with 5 fields:
```
minute hour day_of_month month day_of_week
```

### Field Reference

| Field | Range | Special Characters |
|-------|-------|-------------------|
| Minute | 0-59 | *, -, ,, / |
| Hour | 0-23 | *, -, ,, / |
| Day of Month | 1-31 | *, -, ,, /, ? |
| Month | 1-12 | *, -, ,, / (or names: jan-dec) |
| Day of Week | 0-6 | *, -, ,, /, ? (0=Sunday, 6=Saturday, or names: sun-sat) |

### Special Characters

- **`*`** - Any value (all possible values in the field)
- **`?`** - No specific value (used for day of month or day of week)
- **`-`** - Range of values (e.g., `1-5` means 1, 2, 3, 4, 5)
- **`,`** - List of values (e.g., `1,3,5`)
- **`/`** - Step values (e.g., `*/15` every 15 units, `0-30/5` every 5 from 0 to 30)

### Common Examples

| Expression | Description |
|-----------|-------------|
| `0 9 * * *` | Every day at 9:00 AM |
| `0 0 * * *` | Every day at midnight |
| `0 12 * * *` | Every day at noon |
| `*/15 * * * *` | Every 15 minutes |
| `0 */4 * * *` | Every 4 hours |
| `0 9 1 * *` | First day of every month at 9 AM |
| `0 9 * * 1` | Every Monday at 9 AM |
| `0 9 * * 1-5` | Every weekday (Mon-Fri) at 9 AM |
| `0 18 * * 1,3,5` | Monday, Wednesday, Friday at 6 PM |
| `0 9 * * mon` | Every Monday at 9 AM (using names) |
| `30 2 15 * *` | 2:30 AM on the 15th of each month |

## Available Task Commands

### Predefined Tasks

The system includes these built-in task handlers:

1. **`task:hello_world`**
   - Prints a hello message with timestamp
   - Useful for testing

2. **`task:log_status`**
   - Logs application status with timestamp
   - Useful for monitoring

3. **`task:write_log_file`**
   - Writes a log entry to `app/tmp/cron_tasks.log`
   - Useful for record keeping

### Custom Commands

You can create custom task handlers by:

1. Adding methods to `TaskService` class in `app/libraries/cron/task_service.py`
2. Adding them to the `get_all_handlers()` dictionary

Example:
```python
@staticmethod
def my_custom_task() -> None:
    """My custom task."""
    status.success("Custom task executed!")

# Add to get_all_handlers():
"task:my_custom_task": TaskService.my_custom_task,
```

## Module Interface

### Main Menu

- **Create New Task** - Add a new scheduled task
- **View Task Details** - See detailed information about a task
- **Edit Task** - Modify an existing task's expression or command
- **Delete Task** - Remove a task from the schedule
- **Toggle Task Status** - Enable/disable a task
- **Back** - Return to main menu

### Task Details Display

Shows:
- Task name
- Cron expression
- Command to execute
- Enabled/disabled status
- Last run time
- Next scheduled run time

## Background Execution

- Tasks are checked every 5 seconds
- When a task's scheduled time arrives, it automatically executes
- Execution results are logged to console with `[CRON]` prefix
- Prevents overlapping executions of the same task using locks
- Gracefully handles task failures with error logging

## Configuration

Tasks are persisted in `app/config.json` under the `"cron_tasks"` section:

```json
{
  "cron_tasks": [
    {
      "name": "Daily Report",
      "expression": "0 9 * * *",
      "command": "task:log_status",
      "enabled": true,
      "last_run": "2026-04-28T09:00:00",
      "next_run": "2026-04-29T09:00:00"
    }
  ]
}
```

## Architecture

### Components

1. **`CronExpression`** (`cron_scheduler.py`)
   - Parses and validates cron expressions
   - Determines if a datetime matches the expression
   - Calculates next run times

2. **`CronTask`** (`cron_scheduler.py`)
   - Represents a single scheduled task
   - Tracks enabled status, last run, and next run
   - Converts to/from dictionary for persistence

3. **`CronScheduler`** (`cron_scheduler.py`)
   - Manages a collection of tasks
   - Registers execution callbacks
   - Provides task querying and filtering

4. **`TaskExecutor`** (`task_executor.py`)
   - Runs in background thread
   - Checks for due tasks periodically
   - Prevents overlapping task execution
   - Queues execution results

5. **`TaskService`** (`task_service.py`)
   - Provides predefined task handlers
   - Extensible for custom tasks

## Integration

The cron scheduler is integrated into the main application loop:

1. **Initialization** (`app/main.py`)
   - Loads tasks from config at startup
   - Starts background executor thread

2. **Loop Execution**
   - Checks for executed tasks every cycle
   - Logs execution results
   - Updates UI with task status

3. **Cleanup**
   - Stops executor on application exit
   - Saves all tasks to config

## Extending the System

### Adding Custom Tasks

1. Edit `app/libraries/cron/task_service.py`:
   ```python
   @staticmethod
   def my_backup_task() -> None:
       """Backup application data."""
       status.info("Starting backup...")
       # Your backup logic here
       status.success("Backup completed!")
   ```

2. Register in `get_all_handlers()`:
   ```python
   return {
       # ... existing tasks ...
       "task:my_backup_task": TaskService.my_backup_task,
   }
   ```

3. Use the command `task:my_backup_task` when creating tasks

### Advanced: Module-based Tasks

Create module-specific tasks:

```python
# In app/modules/my_module/controller.py
def my_module_task():
    """Task specific to my module."""
    # Your logic here
    pass

# Register with executor (in main.py or module setup)
executor.register_callback("module:my_module_task", my_module_task)
```

## Debugging

Enable debug mode in Settings to see detailed cron scheduler logs:
- Task checks and evaluations
- Execution start/end messages
- Error details and tracebacks

## Limitations and Notes

- Tasks only execute while the application is running
- No persistence across application restarts (tasks are saved but not executed during restart)
- Time is based on system clock
- Background thread runs every 5 seconds (configurable)
- Maximum task name length: 255 characters
- Command strings must be pre-registered with the executor

## Troubleshooting

### Task not executing
- Verify cron expression is valid
- Check that task is enabled (✓ ENABLED status)
- Confirm task command is registered
- Enable debug mode and watch for error messages

### Invalid cron expression errors
- Review the 5-field format: minute hour day month dow
- Check field value ranges
- Use examples above as reference

### Next run shows N/A
- Ensure cron expression is valid
- Task may be disabled
- Check debug logs for expression parsing errors

## Performance Notes

- Background executor uses minimal CPU (checks every 5 seconds)
- Uses threading for non-blocking operation
- Task execution is synchronous per task
- No impact on main UI responsiveness

