from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

_CONFIG_CACHE: dict[str, Any] | None = None
_DEFAULT_VERBOSE = False
_DEFAULT_LLM_CONFIG: dict[str, Any] = {
    "provider": "lmstudio",
    "base_url": "http://127.0.0.1:1234/v1",
    "chat_endpoint": "/chat/completions",
    "model": "local-model",
    "api_key": "not-needed",
    "timeout": 60,
}
_DEFAULT_ADB_CONFIG: dict[str, Any] = {
    "adb_executable": "adb",
    "device_serial": "",
    "timeout": 30,
}
_DEFAULT_OCR_CONFIG: dict[str, Any] = {
    "tesseract_cmd": "tesseract",
    "language": "eng",
    "psm": 3,
    "oem": 3,
    "timeout": 30,
}
_DEFAULT_CONFIG: dict[str, Any] = {
    "verbose": _DEFAULT_VERBOSE,
    "llm": dict(_DEFAULT_LLM_CONFIG),
    "adb": dict(_DEFAULT_ADB_CONFIG),
    "ocr": dict(_DEFAULT_OCR_CONFIG),
    "cron_tasks": [],
}
_TRUE_VALUES = {"true", "1", "yes", "on"}
_FALSE_VALUES = {"false", "0", "no", "off"}


def _parse_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        if value in (0, 1):
            return bool(value)
        return default

    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in _TRUE_VALUES:
            return True
        if normalized in _FALSE_VALUES:
            return False

    return default


def _config_path() -> Path:
    return Path(__file__).resolve().parent.parent / "config.json"


# noinspection PyTypeChecker
def _load_config() -> dict[str, Any]:
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    path = _config_path()
    config_data: dict[str, Any] = {"verbose": _DEFAULT_VERBOSE}
    loaded_data: dict[str, Any] = {}
    should_save = False

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict):
                loaded_data = dict(data)
            else:
                should_save = True
    except (OSError, json.JSONDecodeError):
        should_save = True

    for key, value in loaded_data.items():
        if key not in {"verbose", "llm", "adb", "ocr", "cron_tasks"}:
            config_data[key] = value

    config_data["verbose"] = _parse_bool(
        loaded_data.get("verbose", _DEFAULT_CONFIG["verbose"]),
        default=_DEFAULT_CONFIG["verbose"],
    )

    # noinspection PyTypeChecker
    llm_data = dict(_DEFAULT_LLM_CONFIG)
    raw_llm_data: Any = loaded_data.get("llm")
    if isinstance(raw_llm_data, dict):
        llm_data.update(cast(dict[str, Any], raw_llm_data))
    else:
        should_save = True

    config_data["llm"] = llm_data

    adb_data = dict(_DEFAULT_ADB_CONFIG)
    raw_adb_data: Any = loaded_data.get("adb")
    if isinstance(raw_adb_data, dict):
        adb_data.update(cast(dict[str, Any], raw_adb_data))
    else:
        should_save = True

    config_data["adb"] = adb_data

    ocr_data = dict(_DEFAULT_OCR_CONFIG)
    raw_ocr_data: Any = loaded_data.get("ocr")
    if isinstance(raw_ocr_data, dict):
        ocr_data.update(cast(dict[str, Any], raw_ocr_data))
    else:
        should_save = True

    config_data["ocr"] = ocr_data

    # Load cron tasks
    cron_tasks_data: list[Any] = []
    raw_cron_tasks: Any = loaded_data.get("cron_tasks")
    if isinstance(raw_cron_tasks, list):
        cron_tasks_data = cast(list[Any], raw_cron_tasks)
    else:
        should_save = True

    config_data["cron_tasks"] = cron_tasks_data

    _CONFIG_CACHE = config_data

    if "llm" not in loaded_data:
        should_save = True

    if "adb" not in loaded_data:
        should_save = True

    if "ocr" not in loaded_data:
        should_save = True

    if "cron_tasks" not in loaded_data:
        should_save = True

    if should_save:
        try:
            _save_config(config_data)
        except OSError:
            pass

    return _CONFIG_CACHE


def _save_config(data: dict[str, Any]) -> None:
    path = _config_path()
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        file.write("\n")


def get_verbose() -> bool:
    return bool(_load_config().get("verbose", _DEFAULT_VERBOSE))


def _get_llm_value(key: str, default: Any) -> Any:
    return _get_section_config("llm").get(key, default)


# noinspection PyTypeChecker
def _get_section_config(section: str) -> dict[str, Any]:
    section_config: Any = _load_config().get(section)
    if isinstance(section_config, dict):
        return cast(dict[str, Any], section_config)
    return {}


def _get_section_value(section: str, key: str, default: Any) -> Any:
    return _get_section_config(section).get(key, default)


def get_llm_provider() -> str:
    value = _get_llm_value("provider", _DEFAULT_LLM_CONFIG["provider"])
    return str(value)


def get_llm_base_url() -> str:
    value = _get_llm_value("base_url", _DEFAULT_LLM_CONFIG["base_url"])
    return str(value)


def get_llm_chat_endpoint() -> str:
    value = _get_llm_value("chat_endpoint", _DEFAULT_LLM_CONFIG["chat_endpoint"])
    return str(value)


def get_llm_model() -> str:
    value = _get_llm_value("model", _DEFAULT_LLM_CONFIG["model"])
    return str(value)


def get_llm_api_key() -> str:
    value = _get_llm_value("api_key", _DEFAULT_LLM_CONFIG["api_key"])
    return str(value)


def get_llm_timeout() -> int:
    value = _get_llm_value("timeout", _DEFAULT_LLM_CONFIG["timeout"])
    try:
        timeout = int(value)
    except (TypeError, ValueError):
        timeout = int(_DEFAULT_LLM_CONFIG["timeout"])
    return timeout if timeout > 0 else int(_DEFAULT_LLM_CONFIG["timeout"])


def get_adb_executable() -> str:
    value = _get_section_value("adb", "adb_executable", _DEFAULT_ADB_CONFIG["adb_executable"])
    return str(value)


def get_adb_device_serial() -> str:
    value = _get_section_value("adb", "device_serial", _DEFAULT_ADB_CONFIG["device_serial"])
    return str(value)


def get_adb_timeout() -> int:
    value = _get_section_value("adb", "timeout", _DEFAULT_ADB_CONFIG["timeout"])
    try:
        timeout = int(value)
    except (TypeError, ValueError):
        timeout = int(_DEFAULT_ADB_CONFIG["timeout"])
    return timeout if timeout > 0 else int(_DEFAULT_ADB_CONFIG["timeout"])


def get_tesseract_cmd() -> str:
    value = _get_section_value("ocr", "tesseract_cmd", _DEFAULT_OCR_CONFIG["tesseract_cmd"])
    return str(value)


def get_ocr_language() -> str:
    value = _get_section_value("ocr", "language", _DEFAULT_OCR_CONFIG["language"])
    return str(value)


def get_ocr_psm() -> int:
    value = _get_section_value("ocr", "psm", _DEFAULT_OCR_CONFIG["psm"])
    try:
        psm = int(value)
    except (TypeError, ValueError):
        psm = int(_DEFAULT_OCR_CONFIG["psm"])
    return psm if psm >= 0 else int(_DEFAULT_OCR_CONFIG["psm"])


def get_ocr_oem() -> int:
    value = _get_section_value("ocr", "oem", _DEFAULT_OCR_CONFIG["oem"])
    try:
        oem = int(value)
    except (TypeError, ValueError):
        oem = int(_DEFAULT_OCR_CONFIG["oem"])
    return oem if oem >= 0 else int(_DEFAULT_OCR_CONFIG["oem"])


def get_ocr_timeout() -> int:
    value = _get_section_value("ocr", "timeout", _DEFAULT_OCR_CONFIG["timeout"])
    try:
        timeout = int(value)
    except (TypeError, ValueError):
        timeout = int(_DEFAULT_OCR_CONFIG["timeout"])
    return timeout if timeout > 0 else int(_DEFAULT_OCR_CONFIG["timeout"])


def set_verbose(value: bool) -> bool:
    global _CONFIG_CACHE

    next_config = dict(_load_config())
    next_config["verbose"] = _parse_bool(value, default=_DEFAULT_CONFIG["verbose"])

    try:
        _save_config(next_config)
    except OSError:
        return get_verbose()

    _CONFIG_CACHE = next_config

    return bool(next_config["verbose"])


def toggle_verbose() -> bool:
    return set_verbose(not get_verbose())


def get_cron_tasks() -> list[Any]:
    """Get the list of cron tasks from config."""
    tasks: Any = _load_config().get("cron_tasks")
    if isinstance(tasks, list):
        return cast(list[Any], tasks)
    return []


def save_cron_tasks(tasks: list[Any]) -> bool:
    """Save cron tasks to config."""
    global _CONFIG_CACHE

    next_config = dict(_load_config())
    next_config["cron_tasks"] = tasks

    try:
        _save_config(next_config)
    except OSError:
        return False

    _CONFIG_CACHE = next_config
    return True


