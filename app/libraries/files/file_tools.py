from __future__ import annotations

from pathlib import Path

from app.core import status


class FileTools:
    def read_text_file(self, path: str) -> str:
        try:
            return Path(path).read_text(encoding="utf-8")
        except OSError as exc:
            status.error(f"Failed to read file '{path}': {exc}")
            return ""

    def write_text_file(self, path: str, content: str) -> bool:
        try:
            Path(path).write_text(content, encoding="utf-8")
            return True
        except OSError as exc:
            status.error(f"Failed to write file '{path}': {exc}")
            return False

    def file_exists(self, path: str) -> bool:
        try:
            return Path(path).is_file()
        except OSError as exc:
            status.error(f"Failed to check file '{path}': {exc}")
            return False
