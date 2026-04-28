from __future__ import annotations

from pathlib import Path

from app.core import status
from app.core.menu import Menu
from app.libraries.files.file_tools import FileTools
from app.libraries.text.text_tools import TextTools


def text_tools_demo() -> None:
    text_tools = TextTools()
    sample_text = "welcome to the reusable library layer"

    status.info(f"Sample: {sample_text}")
    status.info(f"Uppercase: {text_tools.uppercase(sample_text)}")
    status.info(f"Lowercase: {text_tools.lowercase(sample_text)}")
    status.info(f"Title Case: {text_tools.title_case(sample_text)}")
    status.info(f"Word Count: {text_tools.word_count(sample_text)}")
    status.info(f"Character Count: {text_tools.character_count(sample_text)}")


def file_tools_demo() -> None:
    file_tools = FileTools()
    app_root = Path(__file__).resolve().parents[2]
    tmp_dir = app_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    demo_file = tmp_dir / "library_demo.txt"
    demo_content = "Library demo file content."

    if not file_tools.write_text_file(str(demo_file), demo_content):
        return

    if not file_tools.file_exists(str(demo_file)):
        status.warning("Demo file was not created.")
        return

    result = file_tools.read_text_file(str(demo_file))
    if result:
        status.success(f"Read from file: {result}")
        return

    status.warning("Demo file was empty.")


def register(menu) -> None:
    submenu = Menu("Library Demo", exit_label="Back", exit_message="")
    submenu.add("Text Tools Demo", text_tools_demo)
    submenu.add("File Tools Demo", file_tools_demo)
    menu.add("Library Demo", submenu.run)
