from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.constants import DEFAULT_PREFERENCES
from app.core.paths import get_settings_file


class SettingsService:
    def __init__(self, settings_file: Path | None = None) -> None:
        self.settings_file = settings_file or get_settings_file()

    def get_preferences(self) -> dict[str, Any]:
        if not self.settings_file.exists():
            return dict(DEFAULT_PREFERENCES)

        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return dict(DEFAULT_PREFERENCES)
            return self._normalize_preferences(data)
        except Exception:
            return dict(DEFAULT_PREFERENCES)

    def set_preferences(self, prefs: dict[str, Any]) -> dict[str, Any]:
        merged = self.get_preferences()
        merged.update({k: v for k, v in prefs.items() if k in DEFAULT_PREFERENCES})
        merged = self._normalize_preferences(merged)
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=True, indent=2)
        return merged

    def _normalize_preferences(self, raw: dict[str, Any]) -> dict[str, Any]:
        prefs = dict(DEFAULT_PREFERENCES)
        prefs.update({k: v for k, v in raw.items() if k in DEFAULT_PREFERENCES})

        if prefs["locale"] not in {"pt-BR", "en-US"}:
            prefs["locale"] = DEFAULT_PREFERENCES["locale"]
        if prefs["theme"] not in {"system", "light", "dark"}:
            prefs["theme"] = DEFAULT_PREFERENCES["theme"]
        if prefs["uiDensity"] != "compact":
            prefs["uiDensity"] = DEFAULT_PREFERENCES["uiDensity"]
        if not isinstance(prefs["lastPreset"], str):
            prefs["lastPreset"] = DEFAULT_PREFERENCES["lastPreset"]

        return prefs
