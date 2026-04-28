from __future__ import annotations

from typing import Optional

from app.libraries.cron import CronScheduler, TaskExecutor

_CRON_SCHEDULER: Optional[CronScheduler] = None
_CRON_EXECUTOR: Optional[TaskExecutor] = None


def set_scheduler(scheduler: CronScheduler) -> None:
    global _CRON_SCHEDULER
    _CRON_SCHEDULER = scheduler


def get_scheduler() -> Optional[CronScheduler]:
    return _CRON_SCHEDULER


def set_executor(executor: TaskExecutor) -> None:
    global _CRON_EXECUTOR
    _CRON_EXECUTOR = executor


def get_executor() -> Optional[TaskExecutor]:
    return _CRON_EXECUTOR

