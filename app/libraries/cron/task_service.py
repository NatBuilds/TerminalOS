"""
Task Service - Provides callable task handlers for cron scheduler.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable

from app.core import status


class TaskService:
    """Provides predefined task handlers for demonstration and testing."""

    @staticmethod
    def hello_world() -> None:
        """Simple hello world task."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status.success(f"[{timestamp}] Hello from scheduled task!")

    @staticmethod
    def log_status() -> None:
        """Log application status."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status.info(f"[{timestamp}] Status check: Application is running.")

    @staticmethod
    def write_log_file() -> None:
        """Write a message to a log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            log_path = Path(__file__).resolve().parents[2] / "tmp" / "cron_tasks.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] Cron task executed\n")
            status.info(f"[{timestamp}] Log entry written.")
        except Exception as e:
            status.error(f"Failed to write log: {e}")

    @staticmethod
    def adb_screenshot_and_read() -> None:
        """Run the screenshot analyzer module without prompting the user."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status.info(f"[{timestamp}] Starting screenshot analysis task...")

        try:
            from app.modules.screenshot_analyzer.controller import adb_screenshot_and_read

            adb_screenshot_and_read()
            status.success(f"[{timestamp}] Screenshot analysis task completed.")
        except Exception as e:
            status.error(f"[{timestamp}] Screenshot analysis task failed: {e}")

    @staticmethod
    def get_all_handlers() -> dict[str, Callable[[], None]]:
        """Get all available task handlers."""
        return {
            "task:hello_world": TaskService.hello_world,
            "task:log_status": TaskService.log_status,
            "task:write_log_file": TaskService.write_log_file,
            "task:adb_screenshot_and_read": TaskService.adb_screenshot_and_read,
        }

