# Contributing to TerminalOS

Thanks for contributing to the TerminalOS modular CLI framework!

This project is designed as a backbone for building modular Python terminal applications with Android device integration via ADB.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/NatBuilds/TerminalOS.git
cd TerminalOS

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt

# Run the application
python run.py
```

## Architecture Rules

- Entry path is `run.py` → `app.main.main()`.
- Main menu is rebuilt every loop, so module changes are picked up at runtime.
- UI rendering goes through `app/core/ui.py`.
- User-facing output/logs go through `app/core/status.py` (`info`, `warning`, `error`, `success`, `debug`).
- Config state should be accessed via `app/core/config.py` getters/setters.
- Use `app/core/menu.py` - handlers are no-arg callables, `0` always exits/back.

## Adding a Module

1. Create `app/modules/<module_name>/controller.py`.
2. Implement `register(menu) -> None`.
3. Add actions with `menu.add("Label", handler)`.
4. Keep handlers no-arg callables (required by `Menu`).

Example:

```python
from __future__ import annotations

from app.core import status


def run() -> None:
    status.success("Hello from my module.")


def register(menu) -> None:
    menu.add("My Action", run)
```

Use `templates/module_template_controller.py` as a starter.

## Controller vs Service Split

- Keep `controller.py` thin (menu wiring + simple flow).
- Put business logic in:
  - `service.py` inside the module, or
  - shared utilities under `app/libraries/*`.

## Configuration and Verbose Mode

- Config file lives at `app/config.json`.
- `config._load_config()` auto-heals missing/invalid config and writes defaults.
- `status.debug(...)` appears only when verbose is enabled.
- Toggle verbose in the `Settings` module or with `config.toggle_verbose()`.

## Manual Verification (Current Project Standard)

There is no formal test suite yet. Validate manually:

1. Run `python run.py`.
2. Open the menu path you modified.
3. Confirm expected status messages are printed.
4. If you touched reload behavior, enable verbose and watch `[DEBUG]` output.

## Pull Request Checklist

- [ ] Feature is implemented in the right layer (`controller.py` vs service/library).
- [ ] New module follows `register(menu)` contract.
- [ ] No direct `print(...)` calls for status output (use `status.*`).
- [ ] Config reads/writes go through `app/core/config.py`.
- [ ] Manual runtime validation completed.
- [ ] Docs updated (`README.md`, this file, or inline comments) if behavior changed.

## Style Notes

- Keep code simple and explicit.
- Prefer small functions.
- Add type hints where practical.
- Avoid coupling modules to each other unless necessary.
- Preserve dynamic loading behavior in `app/main.py`.

## Reporting Issues

When filing an issue, include:

- Python version
- OS (Windows/macOS/Linux)
- Steps to reproduce
- Expected result
- Actual result
- Relevant terminal output
- Check `logs/` directory for application logs

