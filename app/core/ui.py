from __future__ import annotations

import os

from app.core import art, status


def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render(content: str) -> None:
    clear_console()
    art.print_banner()

    if content:
        status.plain(content)
