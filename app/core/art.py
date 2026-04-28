from __future__ import annotations

from pathlib import Path

from app.core import status

_BANNER_CACHE: str | None = None
_FALLBACK_BANNER = "=== Modular CLI ==="


def _banner_path() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "ascii.txt"


def get_banner() -> str | None:
    global _BANNER_CACHE
    if _BANNER_CACHE is not None:
        return _BANNER_CACHE

    try:
        banner = _banner_path().read_text(encoding="utf-8")
        if not banner.strip():
            banner = _FALLBACK_BANNER
    except OSError:
        banner = _FALLBACK_BANNER

    _BANNER_CACHE = banner
    return _BANNER_CACHE


def print_banner() -> None:
    status.success(get_banner().rstrip("\n"), show_prefix=False)
    status.plain("\n")
