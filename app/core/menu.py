from __future__ import annotations

from typing import Callable

from app.core import status, ui


class Menu:
    FRAME_WIDTH = 67

    def __init__(
        self,
        title: str = "Menu",
        exit_label: str = "Exit",
        exit_message: str = "Goodbye.",
    ) -> None:
        self.title = title
        self.exit_label = exit_label
        self.exit_message = exit_message
        self._options: list[tuple[str, Callable[[], None]]] = []

    def add(self, label: str, function: Callable[[], None]) -> None:
        if not callable(function):
            raise ValueError("Menu function must be callable.")
        self._options.append((label, function))

    def _option_lines(self) -> list[str]:
        lines: list[str] = []
        for index, (label, _) in enumerate(self._options, start=1):
            lines.append(f"{index}. {label}")
        lines.append(f"0. {self.exit_label}")
        return lines

    def _framed_title(self) -> str:
        title = self.title.strip()
        if title.startswith("=") and title.endswith("="):
            return title
        width = max(self.FRAME_WIDTH, len(title) + 2)
        return f" {title} ".center(width, "=")

    def render(self) -> str:
        lines = [self.title, "-" * len(self.title)]
        lines.extend(self._option_lines())
        return "\n".join(lines)

    def render_status(self) -> None:
        title_line = self._framed_title()
        status.success(title_line, show_prefix=False)
        for line in self._option_lines():
            status.info(line, show_prefix=False)
        status.success("=" * len(title_line), show_prefix=False)

    def handle(self, choice: str) -> bool:
        value = (choice or "").strip()
        if not value:
            status.warning("Please enter a menu number.")
            return False

        if not value.isdigit():
            status.warning("Invalid input. Enter a number.")
            return False

        number = int(value)
        if number == 0:
            if self.exit_message:
                status.success(self.exit_message)
            return True

        option_index = number - 1
        if option_index < 0 or option_index >= len(self._options):
            status.warning("Option out of range.")
            return False

        label, action = self._options[option_index]
        status.info(f"Running: {label}")

        try:
            action()
        except Exception as exc:
            status.error(f"Option failed: {exc}")
        return False

    def run(self) -> None:
        while True:
            ui.render("-- ")
            self.render_status()
            choice = status.info_input("\nSelect an option: ", show_prefix=False)
            if self.handle(choice):
                break
            status.info_input("\nPress Enter to continue...", show_prefix=False)
