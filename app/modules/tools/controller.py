from __future__ import annotations

from app.core.menu import Menu
from .service import function_a, function_b


def register(menu) -> None:
    submenu = Menu("Tools", exit_label="Back", exit_message="")
    submenu.add("Option A", function_a)
    submenu.add("Option B", function_b)
    menu.add("Tools", submenu.run)
