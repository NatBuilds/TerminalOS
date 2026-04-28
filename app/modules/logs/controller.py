"""
Logs Management Module
======================

Interactive menu for viewing, searching, and managing application logs.
Provides easy access to all logged messages and session statistics.
"""

from __future__ import annotations

from pathlib import Path

from app.core import status
from app.core.menu import Menu
from app.libraries.logging import get_logger, get_stats


def view_current_session_logs() -> None:
    """Display current session's log entries."""
    logger = get_logger()
    stats = get_stats()

    if not logger.log_file or not logger.log_file.exists():
        status.warning("No log file found for current session.")
        return

    status.success(f"Current Session Log: {logger.log_file.name}")
    status.info(f"Messages logged: {stats['total_messages']}")
    status.info(f"Errors: {stats['errors']}, Warnings: {stats['warnings']}")
    status.info("")

    try:
        with logger.log_file.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Show last 50 lines (skip header)
        for line in lines[-50:]:
            status.info(line.rstrip(), show_prefix=False)
    except OSError as exc:
        status.error(f"Failed to read log file: {exc}")


def view_all_logs() -> None:
    """Display list of all available log files."""
    logger = get_logger()
    log_dir = logger.log_dir

    if not log_dir.exists():
        status.warning("Logs directory does not exist yet.")
        return

    log_files = sorted(log_dir.glob("*.log"), reverse=True)

    if not log_files:
        status.warning("No log files found.")
        return

    status.success(f"Available Log Files ({len(log_files)} total):")
    status.info("")

    for log_file in log_files[:20]:  # Show last 20 logs
        file_size = log_file.stat().st_size
        mod_time = log_file.stat().st_mtime
        from datetime import datetime
        mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")

        size_mb = file_size / 1024 / 1024
        size_str = f"{size_mb:.2f}MB" if size_mb > 1 else f"{file_size/1024:.1f}KB"

        status.info(f"  {log_file.name:30} {size_str:>10}  {mod_date}")


def view_error_summary() -> None:
    """Display summary of all errors from current session."""
    logger = get_logger()
    stats = get_stats()

    if not logger.log_file or not logger.log_file.exists():
        status.warning("No log file found for current session.")
        return

    status.success(f"Error Summary (Current Session)")
    status.info("")

    try:
        with logger.log_file.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        error_lines = [line for line in lines if "[ERROR]" in line]
        warning_lines = [line for line in lines if "[WARNING]" in line]

        if not error_lines and not warning_lines:
            status.success("✓ No errors or warnings in this session!")
            return

        if error_lines:
            status.error(f"Errors ({len(error_lines)}):")
            for line in error_lines[:10]:  # Show first 10 errors
                status.info(f"  {line.rstrip()}", show_prefix=False)
            if len(error_lines) > 10:
                status.info(f"  ... and {len(error_lines) - 10} more", show_prefix=False)

        if warning_lines:
            status.info("")
            status.warning(f"Warnings ({len(warning_lines)}):")
            for line in warning_lines[:10]:  # Show first 10 warnings
                status.info(f"  {line.rstrip()}", show_prefix=False)
            if len(warning_lines) > 10:
                status.info(f"  ... and {len(warning_lines) - 10} more", show_prefix=False)

    except OSError as exc:
        status.error(f"Failed to read log file: {exc}")


def search_logs() -> None:
    """Search for a term in current session's logs."""
    search_term = status.info_input("Enter search term: ", show_prefix=False).strip()

    if not search_term:
        status.warning("Search term cannot be empty.")
        return

    logger = get_logger()
    if not logger.log_file or not logger.log_file.exists():
        status.warning("No log file found for current session.")
        return

    try:
        with logger.log_file.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        matching_lines = [line for line in lines if search_term.lower() in line.lower()]

        if not matching_lines:
            status.warning(f"No matches found for '{search_term}'")
            return

        status.success(f"Found {len(matching_lines)} match(es) for '{search_term}':")
        status.info("")
        for line in matching_lines[:20]:  # Show first 20 matches
            status.info(f"  {line.rstrip()}", show_prefix=False)

        if len(matching_lines) > 20:
            status.info(f"  ... and {len(matching_lines) - 20} more matches", show_prefix=False)

    except OSError as exc:
        status.error(f"Failed to search logs: {exc}")


def show_log_directory() -> None:
    """Show the logs directory location."""
    logger = get_logger()

    status.success(f"Logs Directory:")
    status.info(f"  {logger.log_dir}")

    if logger.log_dir.exists():
        file_count = len(list(logger.log_dir.glob("*.log")))
        total_size = sum(f.stat().st_size for f in logger.log_dir.glob("*.log"))
        size_mb = total_size / 1024 / 1024

        status.success(f"  ✓ Directory exists")
        status.info(f"  Files: {file_count}")
        status.info(f"  Total size: {size_mb:.2f}MB")
    else:
        status.warning(f"  Directory does not exist yet")


def clear_old_logs() -> None:
    """Delete log files older than 30 days."""
    import time

    logger = get_logger()
    log_dir = logger.log_dir

    if not log_dir.exists():
        status.warning("Logs directory does not exist.")
        return

    cutoff_time = time.time() - (30 * 24 * 60 * 60)  # 30 days ago
    deleted_count = 0

    for log_file in log_dir.glob("*.log"):
        if log_file.stat().st_mtime < cutoff_time:
            try:
                log_file.unlink()
                deleted_count += 1
                status.debug(f"Deleted: {log_file.name}")
            except OSError as exc:
                status.error(f"Failed to delete {log_file.name}: {exc}")

    if deleted_count > 0:
        status.success(f"Deleted {deleted_count} old log file(s)")
    else:
        status.info("No old log files to delete")


def show_session_stats() -> None:
    """Display current session statistics."""
    stats = get_stats()

    status.success("Session Statistics:")
    status.info("")
    status.info(f"  Start Time:  {stats['session_start']}")
    status.info(f"  Duration:    {stats['elapsed_seconds']:.1f} seconds")
    status.info(f"  Total Msgs:  {stats['total_messages']}")
    status.info(f"  Errors:      {stats['errors']}")
    status.info(f"  Warnings:    {stats['warnings']}")
    status.info(f"  Log File:    {Path(stats['log_file']).name if stats['log_file'] else 'None'}")


def register(menu) -> None:
    """Register the logs management module with the main menu."""
    submenu = Menu("Logs", exit_label="Back", exit_message="")

    submenu.add("View current session logs", view_current_session_logs)
    submenu.add("View session statistics", show_session_stats)
    submenu.add("View error summary", view_error_summary)
    submenu.add("Search logs", search_logs)
    submenu.add("View all log files", view_all_logs)
    submenu.add("Show logs directory", show_log_directory)
    submenu.add("Clear old logs (>30 days)", clear_old_logs)

    menu.add("Logs", submenu.run)

