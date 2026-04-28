# Quick Start: Cron Scheduler

## Installation

The Cron Scheduler is built-in to TerminalOS. Install via:

```bash
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS
pip install -r requirements.txt
python run.py
```

## Running the Application

```bash
python run.py
```

## Accessing the Cron Scheduler

1. Launch the application
2. From the main menu, select **"Cron Scheduler"**
3. You'll see the Cron Scheduler submenu

## Creating Your First Task

### Example 1: Daily Status Check at 9 AM

1. Select **"Create New Task"**
2. **Task name**: `Daily Status`
3. **Cron expression**: `0 9 * * *`
4. **Command**: `task:log_status`
5. Exit the menu to save

### Example 2: Every 15 Minutes

1. Select **"Create New Task"**
2. **Task name**: `Frequent Check`
3. **Cron expression**: `*/15 * * * *`
4. **Command**: `task:hello_world`
5. Exit the menu to save

### Example 3: Every Weekday at 2:30 PM

1. Select **"Create New Task"**
2. **Task name**: `Weekday Report`
3. **Cron expression**: `30 14 * * 1-5`
4. **Command**: `task:log_status`
5. Exit the menu to save

## Cron Expression Quick Reference

The format is: `minute hour day month day_of_week`

### Quick Examples

| What You Want | Expression | Explanation |
|--------------|-----------|-------------|
| Every day at 9 AM | `0 9 * * *` | minute=0, hour=9, every day |
| Every 15 minutes | `*/15 * * * *` | Every 15 minute intervals |
| Every hour | `0 * * * *` | Top of every hour |
| Every weekday at 9 AM | `0 9 * * 1-5` | Mon(1)-Fri(5) at 9 AM |
| First day of month | `0 0 1 * *` | Midnight on 1st day |
| Every Monday | `0 9 * * 1` | Every Monday at 9 AM |
| Every 4 hours | `0 */4 * * *` | 12 AM, 4 AM, 8 AM, etc. |

## Built-in Task Commands

| Command | Description |
|---------|-------------|
| `task:hello_world` | Test task - prints hello message |
| `task:log_status` | Log system status |
| `task:write_log_file` | Write entry to log file |

## Managing Your Tasks

### View Task Details
1. Select **"View Task Details"**
2. Choose a task from the list
3. See name, expression, command, status, and run times

### Edit a Task
1. Select **"Edit Task"**
2. Choose a task to modify
3. Update the expression and/or command

### Delete a Task
1. Select **"Delete Task"**
2. Choose a task to delete
3. Confirm deletion

### Enable/Disable a Task
1. Select **"Toggle Task Status"**
2. Choose a task
3. Task status flips between enabled/disabled

## Understanding Cron Expressions

### Field Breakdown

```
Minute (0-59)  Hour (0-23)  Day (1-31)  Month (1-12)  Day of Week (0-6)
     0                9          *           *              *
```

### Special Characters

- **`*`** = Every value in that field
- **`?`** = No specific value (for day or day of week)
- **`-`** = Range (e.g., 1-5 means 1,2,3,4,5)
- **`,`** = List (e.g., 1,3,5 means 1, 3, and 5)
- **`/`** = Step (e.g., */5 means every 5)

### More Examples

| Expression | When it runs |
|-----------|-------------|
| `0 0 * * *` | Every day at midnight |
| `0 12 * * *` | Every day at noon |
| `30 9 * * *` | Every day at 9:30 AM |
| `0 * * * *` | Every hour at the top |
| `*/30 * * * *` | Every 30 minutes |
| `0 9-17 * * *` | Every hour 9 AM - 5 PM |
| `0 9 1 * *` | 9 AM on 1st of month |
| `0 0 * * 0` | Every Sunday at midnight |
| `0 9 * * 1-5` | Weekdays at 9 AM |

## Monitoring Task Execution

1. Enable **Debug Mode** in Settings menu
2. Tasks will show `[CRON]` prefixed messages when they execute
3. Check the logs in `logs/` directory for execution history

## Where Tasks Are Saved

Tasks are saved in `app/config.json` under the `"cron_tasks"` section:

```json
{
  "cron_tasks": [
    {
      "name": "Daily Status",
      "expression": "0 9 * * *",
      "command": "task:log_status",
      "enabled": true,
      "last_run": "2026-04-28T09:00:00",
      "next_run": "2026-04-29T09:00:00"
    }
  ]
}
```

## Common Tasks to Create

### Keep Your App Running Healthy
```
Name: Health Check
Expression: 0 */4 * * *
Command: task:log_status
Purpose: Check app status every 4 hours
```

### Keep a Running Log
```
Name: Log Activity
Expression: 0 * * * *
Command: task:write_log_file
Purpose: Log an entry every hour
```

### Morning Briefing
```
Name: Morning Report
Expression: 0 9 * * 1-5
Command: task:log_status
Purpose: Check status every weekday morning
```

## Troubleshooting

### Task Not Running?
- ✓ Is it **enabled**? (Not showing ✗)
- ✓ Is the **expression valid**? (It should have 5 parts)
- ✓ Is the **time correct**? (Check system clock)
- ✓ Is the **app running**? (Tasks only work while app is open)

### Expression Not Valid?
- ✓ Check you have exactly **5 fields** (minute hour day month dow)
- ✓ Check **ranges are valid** (minute 0-59, hour 0-23, etc.)
- ✓ Use the **examples above** as reference

### Can't See Task Updates?
- ✓ **Exit the menu** to save changes to config
- ✓ **Restart the app** if changes don't show up
- ✓ **Check debug logs** to see execution details

## Advanced Features

For advanced usage like creating custom tasks, see:
- **`CRON_SCHEDULER_API.md`** - Full API reference
- **`CRON_SCHEDULER_EXTENDING.md`** - How to add custom tasks
- **`CRON_SCHEDULER_GUIDE.md`** - Complete user guide

## Need Help?

- Run `python test_cron_scheduler.py` to verify system works
- Check logs in `logs/` directory
- Enable Debug mode in Settings
- Read the full guides in documentation files

---

**Happy Scheduling!** ✨

