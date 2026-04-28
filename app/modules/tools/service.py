from __future__ import annotations

from app.core import status


def function_a() -> None:
    status.info("Tools Option A executed.")


def function_b() -> None:
    status.info("Tools Option B executed.")
