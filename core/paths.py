from __future__ import annotations

import os
from pathlib import Path
from shutil import copy2


APP_NAME = "PIT ALERT"
BASE_DIR = Path(__file__).resolve().parent.parent
BUNDLED_CONFIG_PATH = BASE_DIR / "config" / "settings.json"
BUNDLED_CACHE_PATH = BASE_DIR / "data" / "cache" / "forexfactory_thisweek.json"


def get_user_data_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    base_dir = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
    return base_dir / APP_NAME


def get_settings_path() -> Path:
    return get_user_data_dir() / "settings.json"


def get_cache_path() -> Path:
    return get_user_data_dir() / "data" / "cache" / "forexfactory_thisweek.json"


def initialize_user_data() -> Path:
    user_data_dir = get_user_data_dir()
    user_data_dir.mkdir(parents=True, exist_ok=True)

    _copy_if_missing(BUNDLED_CONFIG_PATH, get_settings_path())
    _copy_if_missing(BUNDLED_CACHE_PATH, get_cache_path())

    return user_data_dir


def _copy_if_missing(source: Path, destination: Path) -> None:
    if destination.exists() or not source.exists():
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, destination)
