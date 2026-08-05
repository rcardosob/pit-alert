from __future__ import annotations

import json
import sys
from pathlib import Path
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
    "start_minimized": True,
    "disable_autostart": False,
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


def update_windows_autostart(disable_autostart: bool) -> None:
    """
    Writes/removes the registry value to run PIT ALERT at Windows startup.
    """
    if sys.platform != "win32":
        return

    import winreg

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "PIT_ALERT"
    executable_path = sys.executable

    # In development, use the script path, in production sys.executable is the compiled .exe
    if executable_path.endswith("python.exe") or executable_path.endswith("pythonw.exe"):
        executable_path = str(Path(sys.argv[0]).resolve())

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE
        )
        if not disable_autostart:
            cmd = f'"{executable_path}"'
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error setting registry startup: {e}")
