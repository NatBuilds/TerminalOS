"""
Cron Scheduler Module - UI for managing scheduled tasks.
"""
from app.core.menu import Menu
from app.core import status
from app.core import config
from app.core import cron_runtime
from app.libraries.cron import CronExpression, CronTask, CronScheduler, TaskService
from datetime import datetime


def register(menu: Menu) -> None:
    """Register cron scheduler menu items."""
    menu.add("Cron Scheduler", show_cron_menu)


def show_cron_menu() -> None:
    """Show the cron scheduler submenu."""
    scheduler = cron_runtime.get_scheduler()
    if scheduler is None:
        scheduler = CronScheduler()
        scheduler.load_from_dicts(config.get_cron_tasks())
        cron_runtime.set_scheduler(scheduler)

    while True:
        status.info("")
        status.info("=" * 60)
        status.info("CRON SCHEDULER")
        status.info("=" * 60)

        if scheduler.get_all_tasks():
            status.info(f"\nScheduled Tasks ({len(scheduler.get_all_tasks())}):")
            for i, task in enumerate(scheduler.get_all_tasks(), 1):
                status_str = "✓ ENABLED" if task.enabled else "✗ DISABLED"
                next_run_str = task.next_run.strftime("%Y-%m-%d %H:%M") if task.next_run else "N/A"
                status.info(f"  {i}. {task.name:<20} [{status_str}] Next: {next_run_str}")
        else:
            status.warning("\nNo scheduled tasks configured.")

        status.info("\nOptions:")
        status.info("  1. Create New Task")
        status.info("  2. View Task Details")
        status.info("  3. Edit Task")
        status.info("  4. Delete Task")
        status.info("  5. Toggle Task Status")
        status.info("  0. Back")

        choice = input("\nEnter choice: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            create_task(scheduler)
        elif choice == "2":
            view_task_details(scheduler)
        elif choice == "3":
            edit_task(scheduler)
        elif choice == "4":
            delete_task(scheduler)
        elif choice == "5":
            toggle_task_status(scheduler)
        else:
            status.warning("Invalid choice. Please try again.")

        config.save_cron_tasks(scheduler.to_dicts())

    config.save_cron_tasks(scheduler.to_dicts())
    status.success("Cron tasks saved.")


def create_task(scheduler: CronScheduler) -> None:
    """Create a new cron task."""
    status.info("\n--- Create New Cron Task ---")

    name = input("Enter task name: ").strip()
    if not name:
        status.warning("Task name cannot be empty.")
        return

    # Check for duplicate
    if scheduler.get_task(name):
        status.warning(f"Task '{name}' already exists.")
        return

    status.info("\nEnter cron expression (minute hour day month dow)")
    status.info("Examples:")
    status.info("  0 9 * * *     - Every day at 9:00 AM")
    status.info("  */15 * * * *   - Every 15 minutes")
    status.info("  0 0 1 * *     - First day of every month")
    status.info("  0 9 * * 1     - Every Monday at 9:00 AM")
    status.info("  0 */4 * * *    - Every 4 hours")

    expression = input("Enter cron expression: ").strip()

    # Validate cron expression
    try:
        CronExpression(expression)
    except ValueError as e:
        status.error(f"Invalid cron expression: {e}")
        return

    # Show available commands
    status.info("\nAvailable task commands:")
    task_handlers = TaskService.get_all_handlers()
    for i, command in enumerate(task_handlers.keys(), 1):
        status.info(f"  {i}. {command}")
    status.info("\nOr enter a custom command format:")
    status.info("  'module:function_name'")
    status.info("  'script:path/to/script.py'")

    command = input("Enter command: ").strip()
    if not command:
        status.warning("Command cannot be empty.")
        return

    try:
        task = CronTask(name, expression, command, enabled=True)
        scheduler.add_task(task)
        config.save_cron_tasks(scheduler.to_dicts())
        status.success(f"Task '{name}' created successfully!")
        status.info(f"Next run: {task.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        status.error(f"Failed to create task: {e}")


def view_task_details(scheduler: CronScheduler) -> None:
    """View details of a task."""
    tasks = scheduler.get_all_tasks()
    if not tasks:
        status.warning("No tasks to view.")
        return

    status.info("\nSelect a task to view:")
    for i, task in enumerate(tasks, 1):
        status.info(f"  {i}. {task.name}")

    try:
        choice = int(input("Enter task number: ").strip())
        if 1 <= choice <= len(tasks):
            task = tasks[choice - 1]
            display_task_details(task)
        else:
            status.warning("Invalid selection.")
    except ValueError:
        status.warning("Please enter a valid number.")


def display_task_details(task: CronTask) -> None:
    """Display detailed information about a task."""
    status.info("\n" + "=" * 50)
    status.info("TASK DETAILS")
    status.info("=" * 50)
    status.info(f"Name:       {task.name}")
    status.info(f"Expression: {task.expression}")
    status.info(f"Command:    {task.command}")
    status.info(f"Enabled:    {'Yes' if task.enabled else 'No'}")
    status.info(f"Last Run:   {task.last_run.strftime('%Y-%m-%d %H:%M:%S') if task.last_run else 'Never'}")
    status.info(f"Next Run:   {task.next_run.strftime('%Y-%m-%d %H:%M:%S') if task.next_run else 'N/A'}")
    status.info("=" * 50)


def edit_task(scheduler: CronScheduler) -> None:
    """Edit an existing task."""
    tasks = scheduler.get_all_tasks()
    if not tasks:
        status.warning("No tasks to edit.")
        return

    status.info("\nSelect a task to edit:")
    for i, task in enumerate(tasks, 1):
        status.info(f"  {i}. {task.name}")

    try:
        choice = int(input("Enter task number: ").strip())
        if 1 <= choice <= len(tasks):
            task = tasks[choice - 1]
            edit_task_details(scheduler, task)
            config.save_cron_tasks(scheduler.to_dicts())
        else:
            status.warning("Invalid selection.")
    except ValueError:
        status.warning("Please enter a valid number.")


def edit_task_details(scheduler: CronScheduler, task: CronTask) -> None:
    """Edit details of a specific task."""
    status.info(f"\nEditing task: {task.name}")
    status.info("Leave blank to keep current value.")
    status.info(f"Current expression: {task.expression}")

    expression = input("Enter new cron expression (or press Enter to skip): ").strip()
    if expression:
        try:
            CronExpression(expression)
            task.expression = expression
            task._cron_expr = CronExpression(expression)
            task._update_next_run()
            status.success("Expression updated.")
        except ValueError as e:
            status.error(f"Invalid cron expression: {e}")
            return

    status.info(f"Current command: {task.command}")
    command = input("Enter new command (or press Enter to skip): ").strip()
    if command:
        task.command = command
        status.success("Command updated.")

    status.success("Task updated successfully!")


def delete_task(scheduler: CronScheduler) -> None:
    """Delete a task."""
    tasks = scheduler.get_all_tasks()
    if not tasks:
        status.warning("No tasks to delete.")
        return

    status.info("\nSelect a task to delete:")
    for i, task in enumerate(tasks, 1):
        status.info(f"  {i}. {task.name}")

    try:
        choice = int(input("Enter task number: ").strip())
        if 1 <= choice <= len(tasks):
            task = tasks[choice - 1]
            confirm = input(f"Are you sure you want to delete '{task.name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                scheduler.remove_task(task.name)
                config.save_cron_tasks(scheduler.to_dicts())
                status.success(f"Task '{task.name}' deleted successfully!")
            else:
                status.info("Deletion cancelled.")
        else:
            status.warning("Invalid selection.")
    except ValueError:
        status.warning("Please enter a valid number.")


def toggle_task_status(scheduler: CronScheduler) -> None:
    """Toggle task enabled/disabled status."""
    tasks = scheduler.get_all_tasks()
    if not tasks:
        status.warning("No tasks to toggle.")
        return

    status.info("\nSelect a task to toggle:")
    for i, task in enumerate(tasks, 1):
        status_str = "ENABLED" if task.enabled else "DISABLED"
        status.info(f"  {i}. {task.name} [{status_str}]")

    try:
        choice = int(input("Enter task number: ").strip())
        if 1 <= choice <= len(tasks):
            task = tasks[choice - 1]
            task.enabled = not task.enabled
            status_str = "enabled" if task.enabled else "disabled"
            config.save_cron_tasks(scheduler.to_dicts())
            status.success(f"Task '{task.name}' is now {status_str}.")
        else:
            status.warning("Invalid selection.")
    except ValueError:
        status.warning("Please enter a valid number.")



