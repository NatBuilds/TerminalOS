"""
Task execution service for running cron tasks with proper error handling and logging.
"""
import threading
import time
import traceback
from typing import Callable, Dict, Optional
from queue import Queue
from app.core import status
from app.libraries.cron import CronScheduler, CronTask


class TaskExecutor:
    """Handles background execution of cron tasks."""

    def __init__(self, scheduler: CronScheduler):
        """
        Initialize the task executor.

        Args:
            scheduler: CronScheduler instance to manage tasks
        """
        self.scheduler = scheduler
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.result_queue: Queue = Queue()
        self._task_locks: Dict[str, threading.Lock] = {}

    def register_callback(self, command: str, callback: Callable) -> None:
        """
        Register a callback for a specific command.

        Args:
            command: Command identifier
            callback: Callable to execute
        """
        self.scheduler.register_callback(command, callback)

    def start(self) -> None:
        """Start the background task execution thread."""
        if self.running:
            status.warning("Task executor is already running.")
            return

        self.running = True
        self.thread = threading.Thread(target=self._execution_loop, daemon=True)
        self.thread.start()
        status.debug("Task executor started.")

    def stop(self) -> None:
        """Stop the background task execution thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        status.debug("Task executor stopped.")

    def _execution_loop(self) -> None:
        """Main execution loop for checking and running tasks."""
        while self.running:
            try:
                # Check for due tasks
                due_tasks = self.scheduler.get_due_tasks()
                for task in due_tasks:
                    self._execute_task_safe(task)
            except Exception as e:
                status.debug(f"Error in execution loop: {e}")

            # Sleep to avoid busy waiting
            time.sleep(5)  # Check every 5 seconds

    def _execute_task_safe(self, task: CronTask) -> None:
        """
        Execute a task safely with error handling.

        Args:
            task: Task to execute
        """
        # Prevent overlapping executions
        if task.name not in self._task_locks:
            self._task_locks[task.name] = threading.Lock()

        lock = self._task_locks[task.name]
        if not lock.acquire(blocking=False):
            status.debug(f"Task '{task.name}' is already running, skipping.")
            return

        try:
            self._execute_task(task)
        finally:
            lock.release()

    def _execute_task(self, task: CronTask) -> None:
        """
        Execute a task and handle results.

        Args:
            task: Task to execute
        """
        try:
            status.info(f"[CRON] Executing task: {task.name}")

            # Execute via scheduler (which uses registered callbacks)
            success = self.scheduler.execute_task(task)

            if success:
                status.success(f"[CRON] Task '{task.name}' completed successfully.")
                self.result_queue.put({'task': task.name, 'status': 'success'})
            else:
                status.warning(f"[CRON] Task '{task.name}' command not registered.")
                self.result_queue.put({'task': task.name, 'status': 'not_registered'})

        except Exception as e:
            status.error(f"[CRON] Task '{task.name}' failed: {e}")
            status.debug(f"Traceback: {traceback.format_exc()}")
            self.result_queue.put({'task': task.name, 'status': 'failed', 'error': str(e)})

    def get_results(self) -> list:
        """
        Get all task execution results from the queue.

        Returns:
            List of result dictionaries
        """
        results = []
        while not self.result_queue.empty():
            try:
                results.append(self.result_queue.get_nowait())
            except:
                break
        return results

    def is_running(self) -> bool:
        """Check if executor is running."""
        return self.running and (self.thread is not None and self.thread.is_alive())

