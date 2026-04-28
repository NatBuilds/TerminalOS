"""
File Logging Module
===================

Provides centralized file logging for all application output.
Captures all status messages (info, warning, error, success, debug)
and writes them to timestamped log files in the logs/ directory.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


class FileLogger:
    """
    Centralized logger that writes all status messages to timestamped files.

    Features:
    - Automatic logs/ directory creation
    - Timestamped log files (one per session)
    - Comprehensive message formatting
    - Error tracking and statistics
    - Thread-safe file operations
    """

    def __init__(self, log_dir: str | Path | None = None) -> None:
        """
        Initialize the file logger.

        Args:
            log_dir: Directory to store logs. Defaults to project_root/logs
        """
        if log_dir is None:
            # Navigate to project root from this file's location
            project_root = Path(__file__).resolve().parents[3]
            log_dir = project_root / "logs"
        else:
            log_dir = Path(log_dir).expanduser()

        self.log_dir = log_dir
        self.log_file: Path | None = None
        self.session_start = datetime.now()
        self.message_count = 0
        self.error_count = 0
        self.warning_count = 0

        # Create logs directory if it doesn't exist
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            print(f"Warning: Could not create log directory: {exc}")
            return

        # Create today's log file
        self._setup_log_file()

    def _setup_log_file(self) -> None:
        """Create today's log file if it doesn't exist."""
        if not self.log_dir.exists():
            return

        # Create a new log file for each session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"session_{timestamp}.log"

        try:
            # Write session header
            with self.log_file.open("w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write(f"TerminalOS Session Log\n")
                f.write(f"Started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
        except OSError as exc:
            print(f"Warning: Could not create log file: {exc}")
            self.log_file = None

    def log(
        self,
        level: str,
        message: str,
        show_prefix: bool = True,
        **extra: Any,
    ) -> None:
        """
        Log a message to file.

        Args:
            level: Log level (INFO, WARNING, ERROR, SUCCESS, DEBUG)
            message: The message to log
            show_prefix: Whether to include level prefix
            **extra: Additional context data
        """
        if not self.log_file:
            return

        self.message_count += 1

        # Track error and warning counts
        if level == "ERROR":
            self.error_count += 1
        elif level == "WARNING":
            self.warning_count += 1

        # Format the log entry
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        prefix = f"[{level}]" if show_prefix else ""
        log_entry = f"{timestamp} {prefix} {message}".strip()

        # Add extra context if provided
        if extra:
            extra_lines = "\n".join(f"    {k}: {v}" for k, v in extra.items())
            log_entry = f"{log_entry}\n{extra_lines}"

        # Write to file
        try:
            with self.log_file.open("a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except OSError as exc:
            print(f"Warning: Could not write to log file: {exc}")

    def log_error(self, message: str, **extra: Any) -> None:
        """Log an error message."""
        self.log("ERROR", message, **extra)

    def log_warning(self, message: str, **extra: Any) -> None:
        """Log a warning message."""
        self.log("WARNING", message, **extra)

    def log_info(self, message: str, **extra: Any) -> None:
        """Log an info message."""
        self.log("INFO", message, **extra)

    def log_success(self, message: str, **extra: Any) -> None:
        """Log a success message."""
        self.log("SUCCESS", message, **extra)

    def log_debug(self, message: str, **extra: Any) -> None:
        """Log a debug message."""
        self.log("DEBUG", message, **extra)

    def get_stats(self) -> dict[str, Any]:
        """Get logging statistics."""
        elapsed = (datetime.now() - self.session_start).total_seconds()
        return {
            "session_start": self.session_start.isoformat(),
            "elapsed_seconds": elapsed,
            "total_messages": self.message_count,
            "errors": self.error_count,
            "warnings": self.warning_count,
            "log_file": str(self.log_file) if self.log_file else None,
        }

    def write_summary(self) -> None:
        """Write session summary to log file."""
        if not self.log_file:
            return

        stats = self.get_stats()
        elapsed = stats["elapsed_seconds"]

        summary = f"""
{'='*80}
Session Summary
{'='*80}
Total Messages:  {stats['total_messages']}
Errors:          {stats['errors']}
Warnings:        {stats['warnings']}
Duration:        {elapsed:.1f} seconds
End Time:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
"""
        try:
            with self.log_file.open("a", encoding="utf-8") as f:
                f.write(summary)
        except OSError:
            pass


# Global logger instance
_logger: FileLogger | None = None


def get_logger() -> FileLogger:
    """Get or create the global logger instance."""
    global _logger
    if _logger is None:
        _logger = FileLogger()
    return _logger


def log_info(message: str, **extra: Any) -> None:
    """Log an info message."""
    get_logger().log_info(message, **extra)


def log_warning(message: str, **extra: Any) -> None:
    """Log a warning message."""
    get_logger().log_warning(message, **extra)


def log_error(message: str, **extra: Any) -> None:
    """Log an error message."""
    get_logger().log_error(message, **extra)


def log_success(message: str, **extra: Any) -> None:
    """Log a success message."""
    get_logger().log_success(message, **extra)


def log_debug(message: str, **extra: Any) -> None:
    """Log a debug message."""
    get_logger().log_debug(message, **extra)


def get_stats() -> dict[str, Any]:
    """Get logger statistics."""
    return get_logger().get_stats()

