from __future__ import annotations

import json
from typing import Any

from core.paths import get_settings_path, initialize_user_data


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
    initialize_user_data()
    config_path = get_settings_path()

    if not config_path.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with config_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(loaded)
        return settings

    except json.JSONDecodeError:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict[str, Any]) -> None:
    initialize_user_data()
    config_path = get_settings_path()

    with config_path.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2, ensure_ascii=False)
