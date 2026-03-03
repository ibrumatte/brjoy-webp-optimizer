from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.core.paths import get_history_file


class HistoryService:
    def __init__(self, history_file: Path | None = None) -> None:
        self.history_file = history_file or get_history_file()

    def append(self, folder: str, success: int, errors: int, total: int) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} | {success}/{total} OK | {errors} errors | {folder}\n"
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(entry)

    def list_history(self, limit: int = 200) -> list[dict[str, str]]:
        if not self.history_file.exists():
            return []

        lines = self.history_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        entries: list[dict[str, str]] = []
        for raw in reversed(lines[-limit:]):
            parts = [part.strip() for part in raw.split("|")]
            if len(parts) < 4:
                entries.append({"raw": raw})
                continue
            entries.append(
                {
                    "timestamp": parts[0],
                    "result": parts[1],
                    "errors": parts[2],
                    "folder": parts[3],
                    "raw": raw,
                }
            )
        return entries

    def clear(self) -> None:
        self.history_file.unlink(missing_ok=True)
