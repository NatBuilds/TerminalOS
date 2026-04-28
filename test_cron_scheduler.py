#!/usr/bin/env python3
"""
Cron Scheduler Test Script
Tests the cron scheduler library and module independently of the UI.
"""
from datetime import datetime, timedelta
from app.libraries.cron import CronExpression, CronTask, CronScheduler, TaskService


def test_cron_expressions():
    """Test cron expression parsing and matching."""
    print("=" * 60)
    print("TESTING CRON EXPRESSIONS")
    print("=" * 60)

    test_cases = [
        ("0 9 * * *", "Every day at 9:00 AM"),
        ("*/15 * * * *", "Every 15 minutes"),
        ("0 0 1 * *", "First day of every month"),
        ("0 9 * * 1", "Every Monday at 9:00 AM"),
        ("0 */4 * * *", "Every 4 hours"),
        ("30 14 * * 1-5", "Every weekday at 2:30 PM"),
    ]

    for expr, description in test_cases:
        try:
            cron = CronExpression(expr)
            next_run = cron.next_run()
            print(f"\n✓ {description}")
            print(f"  Expression: {expr}")
            print(f"  Next run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"\n✗ Failed to parse: {expr}")
            print(f"  Error: {e}")


def test_cron_tasks():
    """Test creating and managing cron tasks."""
    print("\n" + "=" * 60)
    print("TESTING CRON TASKS")
    print("=" * 60)

    scheduler = CronScheduler()

    # Create some test tasks
    tasks = [
        CronTask("Morning Report", "0 9 * * *", "task:log_status", enabled=True),
        CronTask("Hourly Check", "0 * * * *", "task:hello_world", enabled=True),
        CronTask("Daily Backup", "0 2 * * *", "task:write_log_file", enabled=False),
    ]

    for task in tasks:
        scheduler.add_task(task)

    # Display tasks
    print(f"\nCreated {len(scheduler.get_all_tasks())} tasks:")
    for task in scheduler.get_all_tasks():
        status = "✓ ENABLED" if task.enabled else "✗ DISABLED"
        print(f"  {task.name:<20} [{status}]")
        print(f"    Expression: {task.expression}")
        print(f"    Command: {task.command}")
        print(f"    Next run: {task.next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    # Test task retrieval
    print(f"\nRetrieving task by name...")
    task = scheduler.get_task("Morning Report")
    if task:
        print(f"✓ Found task: {task.name}")
    else:
        print(f"✗ Task not found")

    # Test task removal
    print(f"\nRemoving task...")
    if scheduler.remove_task("Daily Backup"):
        print(f"✓ Task removed successfully")
    print(f"Remaining tasks: {len(scheduler.get_all_tasks())}")


def test_task_persistence():
    """Test serialization and deserialization of tasks."""
    print("\n" + "=" * 60)
    print("TESTING TASK PERSISTENCE")
    print("=" * 60)

    # Create original tasks
    original_tasks = [
        CronTask("Task 1", "0 9 * * *", "task:hello_world", enabled=True),
        CronTask("Task 2", "30 14 * * 1-5", "task:log_status", enabled=False),
    ]

    scheduler1 = CronScheduler()
    for task in original_tasks:
        scheduler1.add_task(task)

    # Serialize
    serialized = scheduler1.to_dicts()
    print(f"\nSerialized {len(serialized)} tasks to dictionaries")
    print(f"Sample: {serialized[0]}")

    # Deserialize
    scheduler2 = CronScheduler()
    scheduler2.load_from_dicts(serialized)

    print(f"\nDeserialized {len(scheduler2.get_all_tasks())} tasks")
    for task in scheduler2.get_all_tasks():
        print(f"  ✓ {task.name} - {task.expression}")

    # Verify data integrity
    all_match = True
    for t1, t2 in zip(scheduler1.get_all_tasks(), scheduler2.get_all_tasks()):
        if t1.name != t2.name or t1.expression != t2.expression:
            all_match = False
            break

    print(f"\n✓ Data integrity verified: {all_match}")


def test_task_execution():
    """Test task execution callbacks."""
    print("\n" + "=" * 60)
    print("TESTING TASK EXECUTION")
    print("=" * 60)

    scheduler = CronScheduler()

    # Register task handlers
    handlers = TaskService.get_all_handlers()
    for command, callback in handlers.items():
        scheduler.register_callback(command, callback)

    print(f"\nRegistered {len(handlers)} task handlers:")
    for command in handlers.keys():
        print(f"  ✓ {command}")

    # Create a task with a registered handler
    task = CronTask("Test Execution", "0 9 * * *", "task:hello_world", enabled=True)
    scheduler.add_task(task)

    # Try to execute the task
    print(f"\nExecuting task: {task.name}")
    result = scheduler.execute_task(task)
    print(f"Execution result: {'Success' if result else 'Failed'}")
    print(f"Task last run: {task.last_run}")
    print(f"Task next run: {task.next_run}")


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "CRON SCHEDULER TEST SUITE" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")

    test_cron_expressions()
    test_cron_tasks()
    test_task_persistence()
    test_task_execution()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

