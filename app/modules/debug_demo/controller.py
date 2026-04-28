from __future__ import annotations

from app.core import status


def run() -> None:
    status.info("This is an info message.")
    status.warning("This is a warning message.")
    status.error("This is an error message.")
    status.success("This is a success message.")
    status.debug("This debug message appears only when verbose is enabled.")


def register(menu) -> None:
    menu.add("Debug Demo", run)
