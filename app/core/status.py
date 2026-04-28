from __future__ import annotations

import sys

from colorama import Fore, Style, init

from app.core import config
from app.libraries.logging import get_logger


init(autoreset=True)


def _emit(prefix: str, color: str, message: object, show_prefix: bool = True) -> None:
    text = "" if message is None else str(message)
    label = prefix if show_prefix else ""
    sys.stdout.write(f"{color}{label}{text}{Style.RESET_ALL}\n")
    sys.stdout.flush()

    # Also log to file
    try:
        logger = get_logger()
        level = prefix.strip("[]") if prefix else "INFO"
        logger.log(level, text, show_prefix=show_prefix)
    except Exception:
        pass  # Logging errors shouldn't break the app


def plain(message: object = "") -> None:
    text = "" if message is None else str(message)
    sys.stdout.write(f"{text}\n")
    sys.stdout.flush()


def _prompt(prefix: str, color: str, message: object, show_prefix: bool = True) -> str:
    text = "" if message is None else str(message)
    label = prefix if show_prefix else ""
    return input(f"{color}{label}{text}{Style.RESET_ALL}")


def plain_input(message: object = "") -> str:
    text = "" if message is None else str(message)
    return input(text)


def info(message: object, show_prefix: bool = True) -> None:
    _emit("[INFO] ", Fore.CYAN, message, show_prefix=show_prefix)


def info_input(message: object = "", show_prefix: bool = True) -> str:
    return _prompt("[INFO] ", Fore.CYAN, message, show_prefix=show_prefix)


def warning(message: object, show_prefix: bool = True) -> None:
    _emit("[WARN] ", Fore.YELLOW, message, show_prefix=show_prefix)


def warning_input(message: object = "", show_prefix: bool = True) -> str:
    return _prompt("[WARN] ", Fore.YELLOW, message, show_prefix=show_prefix)


def error(message: object, show_prefix: bool = True) -> None:
    _emit("[ERROR] ", Fore.RED, message, show_prefix=show_prefix)


def danger_input(message: object = "", show_prefix: bool = True) -> str:
    return _prompt("[DANGER] ", Fore.RED, message, show_prefix=show_prefix)


def error_input(message: object = "", show_prefix: bool = True) -> str:
    return _prompt("[ERROR] ", Fore.RED, message, show_prefix=show_prefix)


def success(message: object, show_prefix: bool = True) -> None:
    _emit("[OK] ", Fore.GREEN, message, show_prefix=show_prefix)


def success_input(message: object = "", show_prefix: bool = True) -> str:
    return _prompt("[OK] ", Fore.GREEN, message, show_prefix=show_prefix)


def debug(message: object, show_prefix: bool = True) -> None:
    if config.get_verbose():
        _emit("[DEBUG] ", Fore.MAGENTA, message, show_prefix=show_prefix)


def write_log_summary() -> None:
    """Write session summary to log file."""
    try:
        logger = get_logger()
        logger.write_summary()
    except Exception:
        pass


def debug_input(message: object = "", show_prefix: bool = True) -> str:
    return _prompt("[DEBUG] ", Fore.MAGENTA, message, show_prefix=show_prefix)

