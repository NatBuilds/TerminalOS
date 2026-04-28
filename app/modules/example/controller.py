from __future__ import annotations

from app.core import status


def register(menu) -> None:
    menu.add("Say Hello", run)


def run() -> None:
    status.success("Hello from the example module.")
