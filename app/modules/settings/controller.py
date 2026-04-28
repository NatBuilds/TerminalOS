from __future__ import annotations

from app.core import config, status
from app.core.menu import Menu


def show_verbose_state() -> None:
    state = "ON" if config.get_verbose() else "OFF"
    status.info(f"Verbose is {state}.")


def toggle_verbose() -> None:
    state = "ON" if config.toggle_verbose() else "OFF"
    status.success(f"Verbose set to {state}.")


def register(menu) -> None:
    submenu = Menu("Settings", exit_label="Back", exit_message="")
    submenu.add("Toggle verbose", toggle_verbose)
    submenu.add("Show current verbose state", show_verbose_state)
    menu.add("Settings", submenu.run)
