from __future__ import annotations

from pathlib import Path

from .constants import APP_DATA_DIRNAME


def get_app_data_dir() -> Path:
    app_data = Path.home() / APP_DATA_DIRNAME
    app_data.mkdir(parents=True, exist_ok=True)
    return app_data


def get_reports_dir() -> Path:
    reports_dir = get_app_data_dir() / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir


def get_history_file() -> Path:
    return get_app_data_dir() / "history.txt"


def get_settings_file() -> Path:
    return get_app_data_dir() / "settings.json"
