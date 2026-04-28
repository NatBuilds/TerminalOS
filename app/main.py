from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType

from app.core import config, status, ui
from app.core import cron_runtime
from app.core.menu import Menu
from app.libraries.cron import CronScheduler, TaskExecutor, TaskService

APP_ROOT = Path(__file__).resolve().parent
MODULES_ROOT = APP_ROOT / "modules"
LIBRARIES_PREFIX = "app.libraries"


def discover_module_names() -> list[str]:
    if not MODULES_ROOT.exists():
        status.warning("Modules directory not found.")
        return []

    module_names: list[str] = []
    for module_dir in sorted(MODULES_ROOT.iterdir()):
        if not module_dir.is_dir():
            continue
        if (module_dir / "controller.py").exists():
            module_names.append(f"app.modules.{module_dir.name}.controller")

    return module_names


def reload_library_modules() -> None:
    library_names = [
        name
        for name in sys.modules
        if name == LIBRARIES_PREFIX or name.startswith(f"{LIBRARIES_PREFIX}.")
    ]

    for library_name in sorted(library_names, key=lambda name: name.count("."), reverse=True):
        library_module = sys.modules.get(library_name)
        if library_module is None:
            continue

        try:
            importlib.reload(library_module)
        except Exception as exc:
            status.warning(f"Failed to reload library module '{library_name}': {exc}")


def _reload_related_submodules(module_name: str) -> None:
    package_prefix = module_name.rsplit(".", 1)[0] + "."
    related_names = [
        name for name in sys.modules if name.startswith(package_prefix) and name != module_name
    ]

    for related_name in sorted(related_names, key=lambda name: name.count("."), reverse=True):
        related_module = sys.modules.get(related_name)
        if related_module is None:
            continue

        try:
            importlib.reload(related_module)
        except Exception as exc:
            status.error(f"Failed to reload module '{related_name}': {exc}")


def load_or_reload_module(
    module_name: str,
    loaded_modules: dict[str, ModuleType],
) -> ModuleType | None:
    module_key = module_name.split(".")[-2]

    try:
        if module_name in loaded_modules:
            _reload_related_submodules(module_name)
            loaded_modules[module_name] = importlib.reload(loaded_modules[module_name])
        else:
            loaded_modules[module_name] = importlib.import_module(module_name)
    except Exception as exc:
        status.error(f"Failed to load module '{module_key}': {exc}")
        return None

    status.debug(f"Loaded module: {module_key}")
    return loaded_modules[module_name]


def reload_discovered_modules(
    loaded_modules: dict[str, ModuleType],
) -> list[ModuleType]:
    reload_library_modules()
    discovered_names = discover_module_names()

    for stale_name in list(loaded_modules):
        if stale_name not in discovered_names:
            loaded_modules.pop(stale_name, None)

    active_modules: list[ModuleType] = []
    for module_name in discovered_names:
        module = load_or_reload_module(module_name, loaded_modules)
        if module is not None:
            active_modules.append(module)

    return active_modules


def register_modules(menu: Menu, modules: list[ModuleType]) -> None:
    for module in modules:
        module_key = module.__name__.split(".")[-2]
        register = getattr(module, "register", None)
        if not callable(register):
            status.warning(f"Module '{module_key}' has no register(menu) function.")
            continue

        try:
            register(menu)
        except Exception as exc:
            status.error(f"Module '{module_key}' registration failed: {exc}")


def build_menu(loaded_modules: dict[str, ModuleType]) -> Menu:
    menu = Menu("Main Menu")
    modules = reload_discovered_modules(loaded_modules)
    register_modules(menu, modules)
    return menu


def main() -> None:
    config.get_verbose()

    loaded_modules: dict[str, ModuleType] = {}

    # Initialize cron scheduler and executor
    scheduler = CronScheduler()
    executor = TaskExecutor(scheduler)
    cron_runtime.set_scheduler(scheduler)
    cron_runtime.set_executor(executor)

    # Load initial cron tasks
    tasks_data = config.get_cron_tasks()
    scheduler.load_from_dicts(tasks_data)

    # Register built-in cron task handlers before the executor starts.
    for command, callback in TaskService.get_all_handlers().items():
        executor.register_callback(command, callback)

    # Start background task execution
    executor.start()

    try:
        while True:
            # Check for executed tasks and log results
            results = executor.get_results()
            for result in results:
                status.debug(f"Task result: {result}")

            menu = build_menu(loaded_modules)
            ui.render("\n")
            menu.render_status()
            choice = status.info_input("\nSelect an option: ", show_prefix=False)
            if menu.handle(choice):
                break
            status.info_input("\nPress Enter to continue...", show_prefix=False)
    finally:
        # Stop executor and save tasks
        executor.stop()
        config.save_cron_tasks(scheduler.to_dicts())

    # Write session summary to log file
    status.write_log_summary()


if __name__ == "__main__":
    main()
