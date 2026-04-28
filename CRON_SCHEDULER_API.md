# Cron Scheduler Library API Reference

## Installation

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
pip install -r requirements.txt
python run.py
```

Navigate to: **Cron Scheduler** in the main menu

## Overview

The Cron Scheduler library provides a modular, extensible system for scheduling and executing tasks using standard cron expressions. It's designed to integrate seamlessly with the TerminalOS application architecture.

## Components

### 1. CronExpression

Parses and evaluates standard cron expressions.

#### Constructor

```python
CronExpression(expression: str)
```

**Parameters:**
- `expression` (str): A 5-field cron expression (minute hour day month dow)

**Raises:**
- `ValueError`: If the expression format is invalid

**Example:**
```python
from app.libraries.cron import CronExpression

expr = CronExpression("0 9 * * *")  # Every day at 9:00 AM
```

#### Methods

##### `matches(dt: datetime = None) -> bool`

Check if a datetime matches this cron expression.

**Parameters:**
- `dt` (datetime, optional): The datetime to check. Defaults to current time.

**Returns:**
- `bool`: True if the datetime matches the expression

**Example:**
```python
from datetime import datetime

# Check if 9:00 AM today matches "0 9 * * *"
dt = datetime.now().replace(hour=9, minute=0)
if expr.matches(dt):
    print("Task is due!")
```

##### `next_run(from_time: datetime = None) -> datetime`

Calculate the next run time for this expression.

**Parameters:**
- `from_time` (datetime, optional): Start time for calculation. Defaults to now.

**Returns:**
- `datetime`: The next datetime that matches this expression

**Raises:**
- `RuntimeError`: If no match is found within 4 years

**Example:**
```python
next_execution = expr.next_run()
print(f"Next run: {next_execution}")
```

#### Class Attributes

- `MINUTE_RANGE`: range(0, 60)
- `HOUR_RANGE`: range(0, 24)
- `DAY_RANGE`: range(1, 32)
- `MONTH_RANGE`: range(1, 13)
- `DAY_OF_WEEK_RANGE`: range(0, 7)
- `MONTH_NAMES`: Dictionary mapping month names to numbers
- `DAY_NAMES`: Dictionary mapping day names to numbers

---

### 2. CronTask

Represents a single scheduled task with metadata and execution tracking.

#### Constructor

```python
CronTask(name: str, expression: str, command: str, enabled: bool = True)
```

**Parameters:**
- `name` (str): Unique task identifier
- `expression` (str): Cron expression for scheduling
- `command` (str): Command to execute (e.g., "task:hello_world")
- `enabled` (bool, optional): Whether the task is enabled. Defaults to True.

**Raises:**
- `ValueError`: If the cron expression is invalid

**Example:**
```python
from app.libraries.cron import CronTask

task = CronTask(
    name="Daily Report",
    expression="0 9 * * *",
    command="task:log_status",
    enabled=True
)
```

#### Properties

- `name` (str): Task name
- `expression` (str): Cron expression
- `command` (str): Command string
- `enabled` (bool): Whether task is enabled
- `last_run` (Optional[datetime]): Last execution time
- `next_run` (Optional[datetime]): Next scheduled execution time

#### Methods

##### `is_due() -> bool`

Check if this task is due to run now.

**Returns:**
- `bool`: True if task is enabled and its next_run time has passed

**Example:**
```python
if task.is_due():
    scheduler.execute_task(task)
```

##### `mark_run() -> None`

Mark this task as having run and calculate next execution time.

**Example:**
```python
task.mark_run()  # Update last_run and next_run
```

##### `to_dict() -> Dict[str, Any]`

Convert task to dictionary for storage/serialization.

**Returns:**
- `Dict[str, Any]`: Dictionary representation of the task

**Example:**
```python
task_dict = task.to_dict()
# {'name': 'Daily Report', 'expression': '0 9 * * *', ...}
```

##### `from_dict(data: Dict[str, Any]) -> CronTask` (static)

Create a task from a dictionary.

**Parameters:**
- `data` (Dict[str, Any]): Dictionary with task data

**Returns:**
- `CronTask`: New task instance

**Example:**
```python
task_dict = {
    'name': 'Daily Report',
    'expression': '0 9 * * *',
    'command': 'task:log_status',
    'enabled': True,
    'last_run': None,
    'next_run': '2026-04-29T09:00:00'
}
task = CronTask.from_dict(task_dict)
```

---

### 3. CronScheduler

Manages a collection of cron tasks and executes them.

#### Constructor

```python
CronScheduler()
```

**Example:**
```python
from app.libraries.cron import CronScheduler

scheduler = CronScheduler()
```

#### Methods

##### `add_task(task: CronTask) -> None`

Add a task to the scheduler.

**Parameters:**
- `task` (CronTask): Task to add

**Example:**
```python
scheduler.add_task(task)
```

##### `remove_task(name: str) -> bool`

Remove a task by name.

**Parameters:**
- `name` (str): Name of the task to remove

**Returns:**
- `bool`: True if task was removed, False if not found

**Example:**
```python
if scheduler.remove_task("Daily Report"):
    print("Task removed")
```

##### `get_task(name: str) -> Optional[CronTask]`

Get a task by name.

**Parameters:**
- `name` (str): Task name

**Returns:**
- `Optional[CronTask]`: Task if found, None otherwise

**Example:**
```python
task = scheduler.get_task("Daily Report")
if task:
    print(f"Found task: {task.name}")
```

##### `get_all_tasks() -> List[CronTask]`

Get all tasks in the scheduler.

**Returns:**
- `List[CronTask]`: List of all tasks

**Example:**
```python
all_tasks = scheduler.get_all_tasks()
for task in all_tasks:
    print(f"- {task.name}")
```

##### `get_due_tasks() -> List[CronTask]`

Get all tasks that are currently due to run.

**Returns:**
- `List[CronTask]`: List of tasks where is_due() returns True

**Example:**
```python
for task in scheduler.get_due_tasks():
    execute_task_somehow(task)
```

##### `register_callback(command: str, callback: Callable) -> None`

Register a callback function for a specific command.

**Parameters:**
- `command` (str): Command identifier (e.g., "task:hello_world")
- `callback` (Callable): Function to execute when command is called

**Example:**
```python
def my_task():
    print("Running my task!")

scheduler.register_callback("task:my_task", my_task)
```

##### `execute_task(task: CronTask) -> bool`

Execute a task using its registered callback.

**Parameters:**
- `task` (CronTask): Task to execute

**Returns:**
- `bool`: True if execution was successful or deferred

**Example:**
```python
if scheduler.execute_task(task):
    print("Task executed successfully")
```

##### `load_from_dicts(task_dicts: List[Dict[str, Any]]) -> None`

Load tasks from a list of dictionaries (typically from config).

**Parameters:**
- `task_dicts` (List[Dict[str, Any]]): List of task dictionaries

**Example:**
```python
tasks_from_config = [
    {'name': 'Task 1', 'expression': '0 9 * * *', ...}
]
scheduler.load_from_dicts(tasks_from_config)
```

##### `to_dicts() -> List[Dict[str, Any]]`

Convert all tasks to dictionaries for storage.

**Returns:**
- `List[Dict[str, Any]]`: List of task dictionaries

**Example:**
```python
tasks_dicts = scheduler.to_dicts()
config.save_cron_tasks(tasks_dicts)
```

---

### 4. TaskExecutor

Manages background execution of scheduled tasks in a separate thread.

#### Constructor

```python
TaskExecutor(scheduler: CronScheduler)
```

**Parameters:**
- `scheduler` (CronScheduler): Scheduler instance to manage

**Example:**
```python
from app.libraries.cron import TaskExecutor

executor = TaskExecutor(scheduler)
```

#### Methods

##### `register_callback(command: str, callback: Callable) -> None`

Register a callback for a specific command (delegates to scheduler).

**Parameters:**
- `command` (str): Command identifier
- `callback` (Callable): Function to execute

**Example:**
```python
executor.register_callback("task:backup", backup_function)
```

##### `start() -> None`

Start the background task execution thread.

**Side Effects:**
- Spawns a daemon thread that checks for due tasks every 5 seconds
- Logs status messages

**Example:**
```python
executor.start()
print("Task executor started")
```

##### `stop() -> None`

Stop the background task execution thread.

**Side Effects:**
- Signals the thread to stop
- Waits up to 5 seconds for thread to join

**Example:**
```python
executor.stop()
print("Task executor stopped")
```

##### `get_results() -> list`

Get all queued task execution results.

**Returns:**
- `list`: List of result dictionaries

**Result Dictionary Format:**
```python
{
    'task': 'task_name',
    'status': 'success'|'failed'|'not_registered',
    'error': 'error_message'  # Only if status is 'failed'
}
```

**Example:**
```python
results = executor.get_results()
for result in results:
    print(f"Task {result['task']}: {result['status']}")
```

##### `is_running() -> bool`

Check if the executor is actively running.

**Returns:**
- `bool`: True if executor thread is running

**Example:**
```python
if executor.is_running():
    print("Background executor is active")
```

---

### 5. TaskService

Provides built-in task handlers for common operations.

#### Static Methods

##### `hello_world() -> None`

Simple hello world task (for testing).

**Output:**
- Prints "[TIMESTAMP] Hello from scheduled task!" to console

**Example:**
```python
from app.libraries.cron import TaskService

TaskService.hello_world()
```

##### `log_status() -> None`

Log application status.

**Output:**
- Prints "[TIMESTAMP] Status check: Application is running." to console

**Example:**
```python
TaskService.log_status()
```

##### `write_log_file() -> None`

Write a log entry to `app/tmp/cron_tasks.log`.

**Output:**
- Appends "[TIMESTAMP] Cron task executed\n" to log file
- Prints confirmation to console

**Example:**
```python
TaskService.write_log_file()
```

##### `get_all_handlers() -> Dict[str, Callable]`

Get all available task handlers as a dictionary.

**Returns:**
- `Dict[str, Callable]`: Dictionary mapping command strings to handler functions

**Example:**
```python
handlers = TaskService.get_all_handlers()
# {
#     'task:hello_world': <function>,
#     'task:log_status': <function>,
#     'task:write_log_file': <function>
# }
```

---

## Configuration Integration

### Reading Tasks

```python
from app.core import config
from app.libraries.cron import CronScheduler

# Load tasks from config
tasks_data = config.get_cron_tasks()
scheduler = CronScheduler()
scheduler.load_from_dicts(tasks_data)
```

### Saving Tasks

```python
from app.core import config

# Save all scheduler tasks to config
config.save_cron_tasks(scheduler.to_dicts())
```

---

## Complete Example

```python
from app.libraries.cron import (
    CronExpression, CronTask, CronScheduler, 
    TaskExecutor, TaskService
)
from app.core import config

# Create scheduler and executor
scheduler = CronScheduler()
executor = TaskExecutor(scheduler)

# Register all built-in task handlers
for command, callback in TaskService.get_all_handlers().items():
    executor.register_callback(command, callback)

# Create and add a task
task = CronTask(
    name="Morning Check",
    expression="0 9 * * *",
    command="task:log_status",
    enabled=True
)
scheduler.add_task(task)

# Load any previously saved tasks
tasks_data = config.get_cron_tasks()
scheduler.load_from_dicts(tasks_data)

# Start background execution
executor.start()

# ... application runs ...

# Get execution results
results = executor.get_results()
print(f"Executed {len(results)} tasks")

# Save tasks for next session
config.save_cron_tasks(scheduler.to_dicts())

# Stop executor on exit
executor.stop()
```

---

## Cron Expression Syntax Reference

### Supported Operators

| Operator | Example | Meaning |
|----------|---------|---------|
| `*` | `*` | Any value |
| `-` | `1-5` | Range (1,2,3,4,5) |
| `,` | `1,3,5` | List (1,3,5) |
| `/` | `*/5` | Step (every 5) |
| `?` | `?` | No specific value |

### Special Ranges

- **Minutes**: 0-59
- **Hours**: 0-23 (24-hour format)
- **Day of Month**: 1-31
- **Month**: 1-12 or jan-dec
- **Day of Week**: 0-6 (0=Sunday) or sun-sat

### Common Patterns

```
0 0 * * *           - Midnight every day
0 12 * * *          - Noon every day
0 9-17 * * 1-5      - Every hour 9-5, weekdays
*/30 * * * *        - Every 30 minutes
0 0 1 * *           - First day of month
0 0 1 1 *           - New Year's Day
```

---

## Error Handling

### Common Exceptions

```python
# Invalid cron expression
try:
    expr = CronExpression("invalid")
except ValueError as e:
    print(f"Invalid expression: {e}")

# Task not registered
task = CronTask("test", "0 9 * * *", "task:nonexistent")
result = scheduler.execute_task(task)
if not result:
    print("Task command not registered")
```

### Graceful Failure

- Invalid expressions raise `ValueError` at parse time
- Unregistered commands fail silently with `execute_task()` returning `False`
- Executor thread catches all exceptions to prevent thread crashes

