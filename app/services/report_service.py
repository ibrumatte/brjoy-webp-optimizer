from __future__ import annotations

import json
from pathlib import Path

from app.core.paths import get_reports_dir
from app.core.utils import open_path


class ReportService:
    def __init__(self, reports_dir: Path | None = None) -> None:
        self.reports_dir = reports_dir or get_reports_dir()

    def list_reports(self) -> list[dict]:
        if not self.reports_dir.exists():
            return []

        meta_files = sorted(
            self.reports_dir.glob("*/report-meta.json"),
            key=lambda path: path.parent.stat().st_mtime,
            reverse=True,
        )

        reports: list[dict] = []
        for meta_path in meta_files:
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    continue
                reports.append(self._normalize_summary(meta_path.parent, data))
            except Exception:
                continue
        return reports

    def open_report(self, report_id: str, kind: str) -> bool:
        report = self._find_report(report_id)
        if not report:
            return False

        field_map = {
            "html": "html_report",
            "ai": "ai_report",
            "csv": "csv_report",
            "folder": "report_folder",
        }
        target = report.get(field_map.get(kind, ""))
        if not target:
            return False
        target_path = Path(target)
        if not target_path.exists():
            return False
        return open_path(target_path)

    def get_report_preview(self, report_id: str, max_chars: int = 8000) -> str:
        report = self._find_report(report_id)
        if not report:
            return ""
        ai_path = Path(str(report.get("ai_report", "")))
        if not ai_path.exists():
            return ""
        return ai_path.read_text(encoding="utf-8", errors="ignore")[:max_chars]

    def _find_report(self, report_id: str) -> dict | None:
        for report in self.list_reports():
            if report.get("id") == report_id:
                return report
        return None

    def _normalize_summary(self, folder: Path, raw: dict) -> dict:
        report_id = str(raw.get("id") or folder.name)
        generated_at = str(raw.get("generated_at") or raw.get("generatedAt") or "")
        source_folders = list(raw.get("source_folders") or raw.get("sourceFolders") or [])
        output_folders = list(raw.get("output_folders") or raw.get("outputFolders") or [])
        html_report = str(raw.get("html_report") or raw.get("htmlReport") or (folder / "conversion-report.html"))
        ai_report = str(raw.get("ai_report") or raw.get("aiReport") or (folder / "AI-CODE-UPDATE.txt"))
        csv_report = str(raw.get("csv_report") or raw.get("csvReport") or (folder / "conversions.csv"))
        report_folder = str(raw.get("report_folder") or raw.get("reportFolder") or folder)

        summary = {
            "id": report_id,
            "generated_at": generated_at,
            "generatedAt": generated_at,
            "source_folders": source_folders,
            "sourceFolders": source_folders,
            "output_folders": output_folders,
            "outputFolders": output_folders,
            "report_folder": report_folder,
            "reportFolder": report_folder,
            "html_report": html_report,
            "htmlReport": html_report,
            "ai_report": ai_report,
            "aiReport": ai_report,
            "csv_report": csv_report,
            "csvReport": csv_report,
            "success": int(raw.get("success", 0)),
            "errors": int(raw.get("errors", 0)),
            "total": int(raw.get("total", 0)),
            "duration_seconds": float(raw.get("duration_seconds", 0.0)),
            "durationSeconds": float(raw.get("duration_seconds", 0.0)),
            "formato": str(raw.get("formato", "")),
        }
        return summary
