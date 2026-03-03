from __future__ import annotations

import os
import traceback
from threading import current_thread, main_thread
from pathlib import Path
from typing import Any

import tkinter as tk
from tkinter import filedialog

from app.core.constants import APP_NAME, PRESETS, SUPPORTED_EXTENSIONS
from app.core.conversion_engine import ConversionEngine
from app.core.utils import detect_locale
from app.services.history_service import HistoryService
from app.services.report_service import ReportService
from app.services.scan_service import ScanService
from app.services.settings_service import SettingsService


class DesktopAPI:
    def __init__(self) -> None:
        self.settings_service = SettingsService()
        self.history_service = HistoryService()
        self.report_service = ReportService()
        self.scan_service = ScanService()
        self.engine = ConversionEngine(history_service=self.history_service)
        self._window: Any | None = None

    def attach_window(self, window: Any) -> None:
        self._window = window

    # Bootstrap
    def get_app_bootstrap(self) -> dict[str, Any]:
        prefs = self.settings_service.get_preferences()
        locale = prefs.get("locale") or detect_locale()
        return {
            "appName": APP_NAME,
            "locale": locale,
            "preferences": prefs,
            "presets": PRESETS,
            "supportedExtensions": sorted(SUPPORTED_EXTENSIONS),
        }

    # File dialogs
    def pick_files(self) -> list[str]:
        paths = self._pick_files_via_webview()
        if paths is not None:
            return paths
        if current_thread() is not main_thread():
            raise RuntimeError("File dialog unavailable in worker thread")
        root = self._hidden_tk_root()
        filetypes = [("Images", " ".join(f"*{ext}" for ext in sorted(SUPPORTED_EXTENSIONS))), ("All Files", "*.*")]
        paths = filedialog.askopenfilenames(title="Select images", filetypes=filetypes)
        root.destroy()
        return list(paths)

    def pick_folder(self) -> str | None:
        folder = self._pick_folder_via_webview()
        if folder is not None:
            return folder
        if current_thread() is not main_thread():
            raise RuntimeError("Folder dialog unavailable in worker thread")
        root = self._hidden_tk_root()
        folder = filedialog.askdirectory(title="Select folder")
        root.destroy()
        return folder or None

    # Scanning
    def scan_folder(self, root_path: str, extensions: list[str] | None = None) -> list[dict[str, Any]]:
        if not isinstance(root_path, str) or not root_path.strip():
            raise ValueError("root_path must be a non-empty string")
        normalized_extensions = self._normalize_extensions(extensions)
        return self.scan_service.scan_folder(root_path, extensions=normalized_extensions)

    def collect_paths(
        self,
        paths: list[str],
        base_folder: str | None = None,
        extensions: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        if not isinstance(paths, list):
            raise ValueError("paths must be a list")
        sanitized: list[str] = []
        for value in paths:
            if isinstance(value, str) and value.strip():
                sanitized.append(value)
        if not sanitized:
            return []
        if base_folder is not None and not isinstance(base_folder, str):
            raise ValueError("base_folder must be a string or null")
        normalized_extensions = self._normalize_extensions(extensions)
        base = base_folder if isinstance(base_folder, str) and base_folder.strip() else None
        return self.scan_service.collect_paths(sanitized, base_folder=base, extensions=normalized_extensions)

    # Conversion
    def start_conversion(self, payload: dict[str, Any]) -> dict[str, str]:
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object")
        files = payload.get("files")
        config = payload.get("config")
        if not isinstance(files, list):
            raise ValueError("payload.files must be a list")
        if config is None:
            payload = dict(payload)
            payload["config"] = {}
        elif not isinstance(config, dict):
            raise ValueError("payload.config must be an object")
        job_id = self.engine.start_conversion(payload)
        return {"job_id": job_id}

    def get_conversion_status(self, job_id: str) -> dict[str, Any]:
        if not isinstance(job_id, str) or not job_id.strip():
            raise ValueError("job_id must be a non-empty string")
        return self.engine.get_status(job_id)

    def cancel_conversion(self, job_id: str) -> dict[str, bool]:
        if not isinstance(job_id, str) or not job_id.strip():
            raise ValueError("job_id must be a non-empty string")
        canceled = self.engine.cancel(job_id)
        return {"canceled": canceled}

    # Reports
    def list_reports(self) -> list[dict[str, Any]]:
        return self.report_service.list_reports()

    def open_report(self, report_id: str, kind: str) -> dict[str, bool]:
        if not isinstance(report_id, str) or not report_id.strip():
            raise ValueError("report_id must be a non-empty string")
        if kind not in {"html", "ai", "csv", "folder"}:
            raise ValueError("kind must be one of: html, ai, csv, folder")
        ok = self.report_service.open_report(report_id, kind)
        return {"ok": ok}

    def get_report_preview(self, report_id: str, max_chars: int = 8000) -> str:
        return self.report_service.get_report_preview(report_id, max_chars=max_chars)

    # History
    def list_history(self) -> list[dict[str, Any]]:
        return self.history_service.list_history(limit=500)

    def clear_history(self) -> dict[str, bool]:
        self.history_service.clear()
        return {"ok": True}

    # Preferences
    def set_preferences(self, prefs: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(prefs, dict):
            raise ValueError("prefs must be an object")
        merged = self.settings_service.set_preferences(prefs)
        return {"ok": True, "preferences": merged}

    def get_preferences(self) -> dict[str, Any]:
        return self.settings_service.get_preferences()

    # Diagnostics
    def ping(self) -> dict[str, Any]:
        return {
            "ok": True,
            "cwd": os.getcwd(),
        }

    def last_error(self, message: str) -> dict[str, Any]:
        return {
            "ok": False,
            "message": message,
            "trace": traceback.format_exc(),
        }

    def _hidden_tk_root(self) -> tk.Tk:
        if current_thread() is not main_thread():
            raise RuntimeError("Tk dialog fallback can only run on the main thread")
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        return root

    def _pick_files_via_webview(self) -> list[str] | None:
        if self._window is None:
            return None
        try:
            import webview  # type: ignore

            selected = self._window.create_file_dialog(
                webview.OPEN_DIALOG,
                allow_multiple=True,
            )
            if not selected:
                return []
            return [str(path) for path in selected]
        except Exception:
            return None

    def _pick_folder_via_webview(self) -> str | None:
        if self._window is None:
            return None
        try:
            import webview  # type: ignore

            selected = self._window.create_file_dialog(webview.FOLDER_DIALOG)
            if not selected:
                return None
            if isinstance(selected, (list, tuple)):
                return str(selected[0]) if selected else None
            return str(selected)
        except Exception:
            return None

    def _normalize_extensions(self, extensions: list[str] | None) -> list[str] | None:
        if extensions is None:
            return None
        if not isinstance(extensions, list):
            raise ValueError("extensions must be a list or null")
        normalized: list[str] = []
        seen: set[str] = set()
        for raw in extensions:
            if not isinstance(raw, str):
                raise ValueError("extensions must contain only strings")
            value = raw.strip().lower()
            if not value:
                continue
            ext = value if value.startswith(".") else f".{value}"
            if ext not in SUPPORTED_EXTENSIONS:
                raise ValueError(f"unsupported extension filter: {raw}")
            if ext not in seen:
                normalized.append(ext)
                seen.add(ext)
        return normalized or None
