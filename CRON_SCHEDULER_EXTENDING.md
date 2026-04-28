# Extending the Cron Scheduler

## Installation

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
pip install -r requirements.txt
python run.py
```

This guide explains how to extend the Cron Scheduler system with custom tasks and integration patterns.

## Adding Custom Task Handlers

### Method 1: Add to TaskService (Recommended)

For built-in tasks that should be available application-wide:

1. **Edit** `app/libraries/cron/task_service.py`:

```python
@staticmethod
def backup_database() -> None:
    """Backup the application database."""
    from app.core import status
    try:
        status.info("[BACKUP] Starting database backup...")
        # Your backup logic here
        status.success("[BACKUP] Database backup completed!")
    except Exception as e:
        status.error(f"[BACKUP] Backup failed: {e}")
```

2. **Register in `get_all_handlers()`**:

```python
@staticmethod
def get_all_handlers() -> dict[str, callable]:
    """Get all available task handlers."""
    return {
        "task:hello_world": TaskService.hello_world,
        "task:log_status": TaskService.log_status,
        "task:write_log_file": TaskService.write_log_file,
        "task:backup_database": TaskService.backup_database,  # Add this
    }
```

3. **Use in Cron Scheduler**:
   - Create a new task with command `task:backup_database`

### Method 2: Module-Specific Tasks

For tasks tied to a specific module:

**In your module** (`app/modules/my_module/controller.py`):

```python
from app.core import status

def my_module_task():
    """Perform module-specific scheduled action."""
    status.info("[MY_MODULE] Running scheduled task...")
    # Your logic here
    status.success("[MY_MODULE] Task completed!")

def register(menu):
    """Register module menu items."""
    menu.add("My Module", show_my_module_menu)
    
    # Note: Module tasks need to be registered with executor
    # This can be done in main.py or during module initialization
```

**In** `app/main.py` (after creating executor):

```python
# Register module-specific tasks
from app.modules.my_module.controller import my_module_task
executor.register_callback("module:my_module_task", my_module_task)
```

Then use command `module:my_module_task` in cron scheduler.

### Method 3: External Script Execution

For tasks that should run external scripts:

**Create a helper in TaskService**:

```python
@staticmethod
def run_script(script_path: str) -> None:
    """Run an external Python script."""
    import subprocess
    from app.core import status
    
    try:
        status.info(f"[SCRIPT] Running {script_path}...")
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            timeout=60,
            text=True
        )
        if result.returncode == 0:
            status.success(f"[SCRIPT] {script_path} completed")
        else:
            status.error(f"[SCRIPT] {script_path} failed: {result.stderr}")
    except Exception as e:
        status.error(f"[SCRIPT] Failed to run {script_path}: {e}")
```

Register and use:
```python
executor.register_callback("script:my_script", lambda: TaskService.run_script("scripts/my_script.py"))
```

---

## Integration Patterns

### Pattern 1: Database Cleanup

```python
@staticmethod
def cleanup_old_logs() -> None:
    """Delete log files older than 30 days."""
    from app.core import status
    from pathlib import Path
    from datetime import datetime, timedelta
    import os
    
    try:
        logs_dir = Path("logs")
        cutoff = datetime.now() - timedelta(days=30)
        
        deleted = 0
        for log_file in logs_dir.glob("*.log"):
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime < cutoff:
                log_file.unlink()
                deleted += 1
        
        status.info(f"[CLEANUP] Deleted {deleted} old log files")
        status.success("[CLEANUP] Log cleanup completed")
    except Exception as e:
        status.error(f"[CLEANUP] Failed: {e}")
```

**Setup:**
```
Expression: "0 2 * * *"  # 2 AM daily
Command: "task:cleanup_old_logs"
```

### Pattern 2: Health Check

```python
@staticmethod
def health_check() -> None:
    """Perform system health check."""
    from app.core import status
    import psutil
    
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        
        status.info(f"[HEALTH] CPU: {cpu}% | MEM: {mem}%")
        
        if cpu > 80 or mem > 80:
            status.warning(f"[HEALTH] Resource usage high!")
        else:
            status.success("[HEALTH] System healthy")
    except Exception as e:
        status.error(f"[HEALTH] Check failed: {e}")
```

**Setup:**
```
Expression: "*/15 * * * *"  # Every 15 minutes
Command: "task:health_check"
```

### Pattern 3: Email Notifications

```python
@staticmethod
def send_daily_report() -> None:
    """Send daily report via email."""
    from app.core import status
    from app.core import config
    import smtplib
    from email.mime.text import MIMEText
    
    try:
        # Gather report data
        report = build_daily_report()
        
        # Send email
        msg = MIMEText(report)
        msg['Subject'] = 'Daily Report'
        msg['From'] = config.get("email_from")
        msg['To'] = config.get("email_to")
        
        # Connect and send (requires email config in config.json)
        with smtplib.SMTP(config.get("smtp_server")) as server:
            server.send_message(msg)
        
        status.success("[EMAIL] Daily report sent")
    except Exception as e:
        status.error(f"[EMAIL] Failed to send report: {e}")

def build_daily_report() -> str:
    """Generate daily report content."""
    # Your report logic
    return "Daily Report\n..."
```

### Pattern 4: Data Synchronization

```python
@staticmethod
def sync_remote_data() -> None:
    """Sync data with remote server."""
    from app.core import status
    import requests
    
    try:
        status.info("[SYNC] Starting remote sync...")
        
        # Get local data
        local_data = gather_local_data()
        
        # Send to remote
        response = requests.post(
            "https://api.example.com/sync",
            json=local_data,
            timeout=30
        )
        
        if response.status_code == 200:
            status.success("[SYNC] Remote sync completed")
        else:
            status.warning(f"[SYNC] Remote returned {response.status_code}")
    except Exception as e:
        status.error(f"[SYNC] Sync failed: {e}")

def gather_local_data() -> dict:
    """Gather data to sync."""
    # Your data gathering logic
    return {}
```

### Pattern 5: Scheduled Reporting

```python
@staticmethod
def generate_usage_report() -> None:
    """Generate and save usage report."""
    from app.core import status
    from datetime import datetime
    from pathlib import Path
    
    try:
        status.info("[REPORT] Generating usage report...")
        
        # Gather statistics
        stats = {
            'timestamp': datetime.now().isoformat(),
            'usage': calculate_usage_metrics(),
        }
        
        # Save to file
        report_dir = Path("app/tmp/reports")
        report_dir.mkdir(exist_ok=True)
        
        filename = f"report_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(report_dir / filename, 'w') as f:
            import json
            json.dump(stats, f, indent=2)
        
        status.success(f"[REPORT] Saved to {filename}")
    except Exception as e:
        status.error(f"[REPORT] Failed: {e}")

def calculate_usage_metrics() -> dict:
    """Calculate usage metrics."""
    # Your metrics logic
    return {}
```

---

## Testing Custom Tasks

### Unit Test Example

```python
# test_custom_tasks.py
from app.libraries.cron import CronTask, CronScheduler, TaskService

def test_backup_task():
    """Test backup task execution."""
    scheduler = CronScheduler()
    
    # Add custom handler
    scheduler.register_callback("task:backup_database", backup_database)
    
    # Create and execute task
    task = CronTask("Test Backup", "0 2 * * *", "task:backup_database")
    scheduler.add_task(task)
    
    # Execute
    result = scheduler.execute_task(task)
    assert result == True, "Backup task should execute successfully"
    assert task.last_run is not None, "Task should record last run time"

def backup_database():
    """Mock backup function."""
    print("Backup executed!")
```

### Integration Test with Executor

```python
import time
from app.libraries.cron import CronScheduler, TaskExecutor, CronTask

def test_executor():
    """Test background executor."""
    scheduler = CronScheduler()
    executor = TaskExecutor(scheduler)
    
    # Register handler
    call_count = {'count': 0}
    def test_handler():
        call_count['count'] += 1
    
    executor.register_callback("task:test", test_handler)
    
    # Create immediate task (every minute)
    task = CronTask("Test", "* * * * *", "task:test")
    scheduler.add_task(task)
    
    # Start executor
    executor.start()
    time.sleep(6)  # Wait for check cycle
    
    # Get results
    results = executor.get_results()
    
    # Cleanup
    executor.stop()
    
    assert len(results) > 0, "Should have executed at least once"
```

---

## Configuration Extensions

### Adding Task Configuration Section

Update `app/core/config.py` to support task-specific config:

```python
_DEFAULT_TASK_CONFIG: dict[str, Any] = {
    "backup": {
        "enabled": True,
        "retention_days": 30,
    },
    "email": {
        "smtp_server": "smtp.example.com",
        "from_address": "app@example.com",
    }
}

# Add to _DEFAULT_CONFIG:
_DEFAULT_CONFIG = {
    # ... existing config ...
    "task_config": dict(_DEFAULT_TASK_CONFIG),
}
```

### Using Task Config

```python
from app.core import config

def get_task_setting(task_name: str, key: str, default=None):
    """Get a task-specific setting."""
    task_config = config.get_section_config("task_config")
    return task_config.get(task_name, {}).get(key, default)

# In task handler:
retention_days = get_task_setting("backup", "retention_days", 30)
```

---

## Best Practices

1. **Error Handling**: Always wrap task logic in try-except blocks
2. **Logging**: Use `status.info()`, `status.success()`, `status.error()` for visibility
3. **Naming**: Use descriptive task names and command prefixes
4. **Testing**: Test tasks independently before scheduling
5. **Documentation**: Document task purpose, schedule, and requirements
6. **Performance**: Keep task execution time reasonable (< 1 minute recommended)
7. **Concurrency**: Use task.mark_run() to prevent overlapping executions
8. **Persistence**: Save important state to config or files

---

## Troubleshooting

### Task Not Executing

**Check:**
1. Is the task enabled? (toggle in UI)
2. Is the expression valid? (test with test_cron_scheduler.py)
3. Is the command registered? (check executor.register_callback calls)

### Task Executing Too Often

**Check:**
1. Cron expression may be too frequent
2. Clock may have skipped forward
3. Application may have restarted

### Memory Issues with Frequent Tasks

**Solution:**
1. Limit task execution time with `timeout`
2. Clean up resources in task (close files, clear caches)
3. Consider less frequent scheduling

### Task State Not Persisting

**Solution:**
1. Ensure `config.save_cron_tasks()` is called on exit
2. Check that config.json is writable
3. Verify task dictionary serialization with `to_dict()`

