from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "settings.json"


DEFAULT_SETTINGS: dict[str, Any] = {
    "timezone": "America/Mexico_City",
    "active_start": "07:00",
    "active_end": "13:00",
    "alert_minutes_before": 3,
    "currencies": ["USD", "CNY", "GBP", "JPY", "CAD", "EUR", "ALL"],
    "impacts": ["High", "Medium"],
    "sound_enabled": True,
    "auto_close_at_zero": True,
    "popup_width": 520,
    "popup_height": 300,
    "debug_mode": False,
}


def load_settings() -> dict[str, Any]:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not CONFIG_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            loaded = json.load(file)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(loaded)
        return settings

    except json.JSONDecodeError:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict[str, Any]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2, ensure_ascii=False)