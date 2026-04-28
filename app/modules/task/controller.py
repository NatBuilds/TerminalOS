from __future__ import annotations

import time

from app.core import status


def run() -> None:
    status.info("Starting...")
    time.sleep(0.4)
    status.info("Processing...")
    time.sleep(0.4)
    status.info("Finalising...")
    time.sleep(0.4)
    status.success("Done")


def register(menu) -> None:
    menu.add("Run Task", run)
