from __future__ import annotations

import locale
import os
import subprocess
import sys
from pathlib import Path


def open_path(path: str | Path) -> bool:
    target = str(path)
    try:
        if sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os.name == "nt":
            subprocess.Popen(["cmd", "/c", "start", "", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            return False
        return True
    except Exception:
        return False


def detect_locale() -> str:
    loc, _ = locale.getlocale()
    if not loc:
        loc, _ = locale.getdefaultlocale()
    if not loc:
        return "pt-BR"
    lower = str(loc).lower()
    if lower.startswith("pt"):
        return "pt-BR"
    return "en-US"


def format_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
