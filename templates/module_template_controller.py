from __future__ import annotations

"""
Module template for TerminalOS.

How to use:
1) Copy this file to app/modules/<your_module>/controller.py
2) Rename menu labels and handlers
3) Keep register(menu) as the public module contract
"""

from app.core import status
from app.core.menu import Menu


def run_basic_action() -> None:
    status.info("Basic action executed.")


def run_secondary_action() -> None:
    status.success("Secondary action executed.")


def register(menu) -> None:
    # Simple one-line registration:
    # menu.add("My Action", run_basic_action)

    # Submenu registration pattern:
    submenu = Menu("My Module", exit_label="Back", exit_message="")
    submenu.add("Basic Action", run_basic_action)
    submenu.add("Secondary Action", run_secondary_action)
    menu.add("My Module", submenu.run)

