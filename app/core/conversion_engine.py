from __future__ import annotations

import csv
import html
import json
import re
import shutil
import subprocess
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

from app.core.constants import MAX_WORKERS
from app.core.models import ConversionItemStatus, ConversionJob
from app.core.paths import get_reports_dir
from app.services.history_service import HistoryService


class ConversionEngine:
    def __init__(self, history_service: HistoryService | None = None) -> None:
        self.history_service = history_service or HistoryService()
        self.reports_dir = get_reports_dir()
        self._jobs: dict[str, ConversionJob] = {}
        self._lock = threading.Lock()

    def start_conversion(self, payload: dict[str, Any]) -> str:
        files = payload.get("files") or []
        config = payload.get("config") or {}
        if not files:
            raise ValueError("No files provided")
        if not isinstance(files, list):
            raise ValueError("files must be a list")
        if not isinstance(config, dict):
            raise ValueError("config must be an object")

        validated_config = self._normalize_config(config)
        validation_error = self._validate_config(validated_config)
        if validation_error:
            raise ValueError(validation_error)

        job_id = str(uuid.uuid4())
        items: list[ConversionItemStatus] = []
        for index, file in enumerate(files):
            if not isinstance(file, dict):
                raise ValueError(f"Invalid file item at index {index}")

            raw_path = str(file.get("path", "")).strip()
            if not raw_path:
                raise ValueError(f"Invalid file path at index {index}")

            rel_path = str(file.get("relPath") or Path(raw_path).name)
            raw_size = file.get("size")
            size = self._to_int(raw_size)
            if size is None:
                try:
                    size = Path(raw_path).stat().st_size
                except Exception:
                    size = 0

            items.append(
                ConversionItemStatus(
                    id=str(file.get("id") or uuid.uuid4()),
                    path=raw_path,
                    relPath=rel_path,
                    size=size,
                )
            )

        if not items:
            raise ValueError("No valid files provided")
        source_folders = sorted({self._derive_source_root(item.path, item.relPath) for item in items})

        job = ConversionJob(
            id=job_id,
            config=validated_config,
            items=items,
            phase="queued",
            completed=0,
            total=len(items),
            message="Queued",
            startedAt=datetime.now().isoformat(timespec="seconds"),
            sourceFolders=source_folders,
        )

        with self._lock:
            self._jobs[job_id] = job

        thread = threading.Thread(target=self._run_conversion, args=(job_id,), daemon=True)
        thread.start()
        return job_id

    def get_status(self, job_id: str) -> dict[str, Any]:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                raise ValueError("Job not found")
            return {
                "job_id": job.id,
                "phase": job.phase,
                "completed": job.completed,
                "total": job.total,
                "success": job.success,
                "errors": job.errors,
                "skipped": job.skipped,
                "message": job.message,
                "startedAt": job.startedAt,
                "finishedAt": job.finishedAt,
                "durationSeconds": job.durationSeconds,
                "reportId": job.reportId,
                "outputFolder": job.outputFolder,
                "sourceFolders": job.sourceFolders,
                "items": [asdict(item) for item in job.items],
            }

    def cancel(self, job_id: str) -> bool:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return False
            if job.phase in {"done", "error", "canceled"}:
                return False
            job.cancelRequested = True
            job.message = "Cancel requested"
            return True

    def _run_conversion(self, job_id: str) -> None:
        start_time = datetime.now()

        with self._lock:
            job = self._jobs[job_id]
            job.phase = "running"
            job.message = "Converting..."

        config = job.config
        session_folder = self._resolve_session_folder(job, config)
        reserved_paths = set()
        reserve_lock = threading.Lock()
        conversion_details: list[dict[str, Any]] = []

        def worker(idx: int, item: ConversionItemStatus):
            if self._is_cancel_requested(job_id):
                return idx, "skipped", "Canceled", item.size, 0, [], []

            source_path = Path(item.path)
            output_dir = self._resolve_output_folder(source_path, item.relPath, session_folder, config)

            try:
                if config["batch_sizes_enabled"]:
                    total_after = 0
                    outputs: list[str] = []
                    backups: list[str] = []
                    for size in config["batch_sizes"]:
                        if self._is_cancel_requested(job_id):
                            return idx, "skipped", "Canceled", item.size, 0, outputs, backups
                        base = output_dir / f"{source_path.stem}_{size}w.{config['formato']}"
                        out, conflict_message = self._resolve_conflict_path(
                            base,
                            config["conflict_policy"],
                            reserved_paths,
                            reserve_lock,
                        )
                        if out is None:
                            return idx, "skipped", conflict_message, item.size, total_after, outputs, backups
                        size_out, backup_path = self._convert_to_target(
                            source_path=source_path,
                            output_path=out,
                            config=config,
                            width=size,
                        )
                        total_after += size_out
                        outputs.append(str(out))
                        if backup_path:
                            backups.append(backup_path)
                    return idx, "ok", "", item.size, total_after, outputs, backups

                base = output_dir / f"{source_path.stem}.{config['formato']}"
                out, conflict_message = self._resolve_conflict_path(
                    base,
                    config["conflict_policy"],
                    reserved_paths,
                    reserve_lock,
                )
                if out is None:
                    return idx, "skipped", conflict_message, item.size, 0, [], []
                size_after, backup_path = self._convert_to_target(
                    source_path=source_path,
                    output_path=out,
                    config=config,
                )
                backups = [backup_path] if backup_path else []
                return idx, "ok", "", item.size, size_after, [str(out)], backups
            except subprocess.CalledProcessError as exc:
                err = (exc.stderr or str(exc)).strip()
                return idx, "error", err[:180], item.size, 0, [], []
            except Exception as exc:
                return idx, "error", str(exc)[:180], item.size, 0, [], []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(worker, idx, item): idx for idx, item in enumerate(job.items)}

            for future in as_completed(futures):
                idx = futures[future]
                item = job.items[idx]
                try:
                    _, status, error, size_before, size_after, outputs, backups = future.result()
                except Exception as exc:
                    status, error, size_before, size_after, outputs, backups = "error", str(exc), item.size, 0, [], []

                with self._lock:
                    job = self._jobs[job_id]
                    job.completed += 1

                    if status == "ok":
                        item.status = "ok"
                        item.sizeAfter = size_after
                        job.success += 1
                        conversion_details.append(
                            {
                                "file": item.relPath,
                                "source_path": item.path,
                                "output_paths": outputs,
                                "backup_paths": backups,
                                "before": size_before,
                                "after": size_after,
                                "saved": size_before - size_after,
                                "percent": ((size_before - size_after) / size_before * 100) if size_before > 0 else 0,
                            }
                        )
                    elif status == "skipped":
                        item.status = "skipped"
                        item.error = error
                        job.skipped += 1
                    else:
                        item.status = "error"
                        item.error = error or "Unknown error"
                        job.errors += 1

                    if job.cancelRequested and job.phase == "running":
                        job.message = "Canceling..."

                if self._is_cancel_requested(job_id):
                    executor.shutdown(wait=False, cancel_futures=True)
                    break

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        with self._lock:
            job = self._jobs[job_id]
            job.durationSeconds = round(duration, 2)
            job.finishedAt = end_time.isoformat(timespec="seconds")

        if self._is_cancel_requested(job_id):
            with self._lock:
                job = self._jobs[job_id]
                for item in job.items:
                    if item.status == "pending":
                        item.status = "skipped"
                        item.error = "Canceled"
                        job.skipped += 1
                job.phase = "canceled"
                job.message = f"Canceled: {job.success} ok, {job.errors} errors, {job.skipped} skipped"
            return

        if conversion_details:
            try:
                self.history_service.append(session_folder, job.success, job.errors, job.total)
                metadata = self._generate_reports(
                    output_folder=session_folder,
                    details=conversion_details,
                    duration=duration,
                    success=job.success,
                    errors=job.errors,
                    total=job.total,
                    formato=config["formato"],
                    source_folders=job.sourceFolders,
                )
            except Exception as exc:
                metadata = None
                with self._lock:
                    job = self._jobs[job_id]
                    job.message = f"Conversion done, report failed: {exc}"

            with self._lock:
                job = self._jobs[job_id]
                if metadata:
                    job.reportId = metadata.get("id", "")
                    job.outputFolder = metadata.get("output_folder", session_folder)
                job.phase = "done"
                job.message = f"Completed: {job.success} ok, {job.errors} errors"
            return

        with self._lock:
            job = self._jobs[job_id]
            job.phase = "done"
            job.message = "Completed with no converted files"

    def _is_cancel_requested(self, job_id: str) -> bool:
        with self._lock:
            job = self._jobs.get(job_id)
            return bool(job and job.cancelRequested)

    def _normalize_config(self, config: dict[str, Any]) -> dict[str, Any]:
        batch_sizes = config.get("batch_sizes") or []
        if isinstance(batch_sizes, str):
            batch_sizes = [s.strip() for s in batch_sizes.split(",") if s.strip()]

        normalized_sizes: list[int] = []
        for value in batch_sizes:
            try:
                num = int(value)
                if num > 0:
                    normalized_sizes.append(num)
            except Exception:
                continue

        largura = config.get("largura_max")
        altura = config.get("altura_max")

        def to_int(v):
            return self._to_int(v)

        quality = self._to_int(config.get("qualidade"))
        brightness = self._to_int(config.get("brightness"))

        return {
            "formato": str(config.get("formato", "webp")).lower(),
            "redimensionar": bool(config.get("redimensionar", False)),
            "largura_max": to_int(largura),
            "altura_max": to_int(altura),
            "recorte_1x1": bool(config.get("recorte_1x1", False)),
            "qualidade": quality if quality is not None else 85,
            "sharpen": bool(config.get("sharpen", False)),
            "brightness": brightness if brightness is not None else 100,
            "batch_sizes_enabled": bool(config.get("batch_sizes_enabled", False)),
            "batch_sizes": sorted(set(normalized_sizes)),
            "substituir_no_lugar": bool(config.get("substituir_no_lugar", False)),
            "manter_estrutura": bool(config.get("manter_estrutura", True)),
            "output_folder": str(config.get("output_folder", "") or ""),
            "conflict_policy": str(config.get("conflict_policy", "version") or "version").lower(),
            "backup_enabled": bool(config.get("backup_enabled", False)),
            "backup_strategy": str(config.get("backup_strategy", "bak") or "bak").lower(),
        }

    def _to_int(self, value: Any) -> int | None:
        if value in (None, ""):
            return None
        try:
            return int(value)
        except Exception:
            return None

    def _validate_config(self, config: dict[str, Any]) -> str | None:
        if config["formato"] not in {"webp", "png"}:
            return "Invalid output format"
        if config["batch_sizes_enabled"] and not config["batch_sizes"]:
            return "Batch sizes enabled but no valid sizes were provided"
        if config["redimensionar"] and config["largura_max"] is None and not config["batch_sizes_enabled"]:
            return "Resize enabled without valid width"
        if config["altura_max"] is not None and config["largura_max"] is None and not config["batch_sizes_enabled"]:
            return "Height defined without width"
        if not 1 <= config["qualidade"] <= 100:
            return "Quality must be between 1 and 100"
        if not 50 <= config["brightness"] <= 150:
            return "Brightness must be between 50 and 150"
        if config["conflict_policy"] not in {"version", "overwrite", "skip"}:
            return "Invalid conflict policy"
        if config["backup_strategy"] not in {"bak", "folder"}:
            return "Invalid backup strategy"
        return None

    def _resolve_session_folder(self, job: ConversionJob, config: dict[str, Any]) -> str:
        first_parent = str(Path(job.items[0].path).parent)

        if config["substituir_no_lugar"] or config["manter_estrutura"]:
            return first_parent

        if config["output_folder"]:
            out = Path(config["output_folder"]).expanduser().resolve()
            out.mkdir(parents=True, exist_ok=True)
            return str(out)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = Path(first_parent) / f"BrJoy_{timestamp}"
        folder.mkdir(parents=True, exist_ok=True)
        return str(folder)

    def _resolve_output_folder(self, source_path: Path, rel_path: str, session_folder: str, config: dict[str, Any]) -> Path:
        if config["substituir_no_lugar"] or config["manter_estrutura"]:
            source_path.parent.mkdir(parents=True, exist_ok=True)
            return source_path.parent

        session_dir = Path(session_folder)
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir

    def _derive_source_root(self, file_path: str, rel_path: str) -> str:
        source = Path(file_path).resolve()
        rel = PurePosixPath(str(rel_path).replace("\\", "/"))
        strip_levels = max(len(rel.parts) - 1, 0)
        root = source.parent
        for _ in range(strip_levels):
            root = root.parent
        return str(root)

    def _build_convert_cmd(self, input_path: Path, config: dict[str, Any], width: int | None = None) -> list[str]:
        cmd = ["convert", str(input_path)]

        if config["sharpen"]:
            cmd.extend(["-sharpen", "0x1"])

        brightness = config["brightness"]
        if brightness != 100:
            cmd.extend(["-modulate", f"{brightness},100,100"])

        force_width = width is not None
        if force_width or (config["redimensionar"] and config["largura_max"]):
            resize_width = width if force_width else config["largura_max"]
            if config["altura_max"] and not force_width:
                h = config["altura_max"]
                cmd.extend(["-resize", f"{resize_width}x{h}^", "-gravity", "center", "-extent", f"{resize_width}x{h}"])
            elif config["recorte_1x1"]:
                cmd.extend(["-resize", f"{resize_width}x{resize_width}^", "-gravity", "center", "-extent", f"{resize_width}x{resize_width}"])
            else:
                cmd.extend(["-resize", f"{resize_width}x>"])
        elif config["recorte_1x1"]:
            cmd.extend(["-gravity", "center", "-extent", "1:1"])

        cmd.extend(["-quality", str(config["qualidade"])])
        return cmd

    def _reserve_output_path(self, output_path: Path, reserved_paths: set[str], reserve_lock: threading.Lock) -> Path:
        with reserve_lock:
            candidate = output_path
            suffix = 1
            while str(candidate) in reserved_paths or candidate.exists():
                candidate = output_path.with_name(f"{output_path.stem}_{suffix}{output_path.suffix}")
                suffix += 1
            reserved_paths.add(str(candidate))
            return candidate

    def _resolve_conflict_path(
        self,
        output_path: Path,
        conflict_policy: str,
        reserved_paths: set[str],
        reserve_lock: threading.Lock,
    ) -> tuple[Path | None, str]:
        with reserve_lock:
            if conflict_policy == "overwrite":
                if str(output_path) in reserved_paths:
                    return None, "Skipped: duplicate output path in current batch"
                reserved_paths.add(str(output_path))
                return output_path, ""

            if conflict_policy == "skip":
                if str(output_path) in reserved_paths or output_path.exists():
                    return None, "Skipped: output already exists"
                reserved_paths.add(str(output_path))
                return output_path, ""

            candidate = output_path
            suffix = 1
            while str(candidate) in reserved_paths or candidate.exists():
                candidate = output_path.with_name(f"{output_path.stem}_{suffix}{output_path.suffix}")
                suffix += 1
            reserved_paths.add(str(candidate))
            return candidate, ""

    def _convert_to_target(
        self,
        source_path: Path,
        output_path: Path,
        config: dict[str, Any],
        width: int | None = None,
    ) -> tuple[int, str]:
        backup_path = ""
        source_resolved = source_path.resolve()
        output_resolved = output_path.resolve()
        same_file_target = source_resolved == output_resolved

        if config["substituir_no_lugar"] and config["backup_enabled"]:
            backup_target: Path | None = None
            if same_file_target and source_path.exists():
                backup_target = source_path
            elif output_path.exists():
                backup_target = output_path
            if backup_target is not None:
                backup_path = str(self._create_backup(backup_target, config["backup_strategy"]))

        cmd = self._build_convert_cmd(source_path, config, width=width)
        temp_output: Path | None = None
        final_target = output_path
        if same_file_target:
            temp_output = output_path.with_name(f".{output_path.stem}.tmp-{uuid.uuid4().hex}{output_path.suffix}")
            final_target = temp_output
        cmd.append(str(final_target))

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            if temp_output is not None:
                temp_output.replace(output_path)
            size_after = output_path.stat().st_size
            return size_after, backup_path
        finally:
            if temp_output is not None and temp_output.exists():
                temp_output.unlink(missing_ok=True)

    def _create_backup(self, target: Path, strategy: str) -> Path:
        strategy_name = strategy if strategy in {"bak", "folder"} else "bak"

        if strategy_name == "folder":
            backup_dir = target.parent / "_backup"
            backup_dir.mkdir(parents=True, exist_ok=True)
            destination = backup_dir / target.name
        else:
            destination = target.with_name(f"{target.name}.bak")

        if destination.exists():
            suffix = 1
            while True:
                candidate = destination.with_name(f"{destination.name}.{suffix}")
                if not candidate.exists():
                    destination = candidate
                    break
                suffix += 1

        shutil.copy2(target, destination)
        return destination

    def _safe_csv_cell(self, value: str) -> str:
        text = str(value).replace("\r", " ").replace("\n", " ")
        if text.startswith(("=", "+", "-", "@")):
            return "'" + text
        return text

    def _normalize_report_path(self, value: str) -> str:
        return str(value).replace("\r", " ").replace("\n", " ").replace("\\", "/").strip()

    def _build_converted_report_path(self, original_name: str, formato: str) -> tuple[str, str]:
        normalized = self._normalize_report_path(original_name)
        try:
            converted = str(PurePosixPath(normalized).with_suffix(f".{formato}"))
        except ValueError:
            converted = f"{normalized}.{formato}"
        return normalized, converted

    def _sanitize_report_token(self, value: str) -> str:
        token = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower())
        token = re.sub(r"-+", "-", token).strip("-")
        return token[:40] or "session"

    def _create_report_folder(self, output_folder: str) -> Path:
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        source_token = self._sanitize_report_token(Path(output_folder).name)
        folder = self.reports_dir / f"{timestamp}-{source_token}"
        suffix = 1
        while folder.exists():
            folder = self.reports_dir / f"{timestamp}-{source_token}-{suffix}"
            suffix += 1
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def _store_report_metadata(self, metadata: dict[str, Any]) -> Path:
        meta_path = Path(metadata["report_folder"]) / "report-meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=True, indent=2)
        return meta_path

    def _generate_reports(
        self,
        output_folder: str,
        details: list[dict[str, Any]],
        duration: float,
        success: int,
        errors: int,
        total: int,
        formato: str,
        source_folders: list[str] | None = None,
    ) -> dict[str, Any]:
        report_folder = self._create_report_folder(output_folder)
        ai_paths = self._generate_ai_report(report_folder, details, formato)

        resolved_source_folders = sorted({self._normalize_report_path(p) for p in (source_folders or []) if p})
        if not resolved_source_folders:
            resolved_source_folders = sorted({self._normalize_report_path(Path(item["source_path"]).parent) for item in details if item.get("source_path")})
        if not resolved_source_folders:
            resolved_source_folders = [self._normalize_report_path(output_folder)]

        output_folders = sorted({self._normalize_report_path(Path(path).parent) for item in details for path in item.get("output_paths", []) if path})
        if not output_folders:
            output_folders = [self._normalize_report_path(output_folder)]

        total_before = sum(d["before"] for d in details)
        total_after = sum(d["after"] for d in details)
        total_saved = total_before - total_after
        percent_saved = (total_saved / total_before * 100) if total_before > 0 else 0
        errors_percent = (errors / total * 100) if total > 0 else 0
        avg_seconds = (duration / success) if success > 0 else 0
        top_10 = sorted(details, key=lambda x: x["saved"], reverse=True)[:10]

        source_folders_html = "".join(f"<li>{html.escape(folder)}</li>" for folder in resolved_source_folders)
        output_folders_html = "".join(f"<li>{html.escape(folder)}</li>" for folder in output_folders)

        report_html = f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>BrJoy WebP Optimizer - Relatorio</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background:#f5f7fa; padding:20px; color:#142033; }}
        .container {{ max-width:1100px; margin:0 auto; background:#fff; border-radius:14px; overflow:hidden; box-shadow:0 10px 30px rgba(15,23,42,.08); }}
        .header {{ background: linear-gradient(115deg,#131D2F,#1B2940); color:#fff; padding:34px; }}
        .header h1 {{ font-size:34px; margin-bottom:6px; }}
        .stats {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap:14px; padding:24px; }}
        .card {{ background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:16px; }}
        .card h3 {{ font-size:13px; color:#566476; margin-bottom:8px; }}
        .value {{ font-size:28px; font-weight:700; }}
        .ok {{ color:#15C39A; }}
        .err {{ color:#dc2626; }}
        .save {{ color:#2B6FE4; }}
        .section {{ padding: 0 24px 24px; }}
        table {{ width:100%; border-collapse:collapse; margin-top:10px; }}
        th,td {{ text-align:left; padding:10px; border-bottom:1px solid #e5edf5; }}
        th {{ background:#f8fafc; font-size:12px; text-transform:uppercase; color:#566476; }}
        .size,.saving {{ text-align:right; }}
        .saving {{ color:#15C39A; font-weight:600; }}
        .paths {{ margin-left:20px; margin-top:8px; }}
        .paths li {{ margin-bottom:4px; font-family:'Courier New', monospace; }}
        .footer {{ padding:20px 24px 24px; background:#f8fafc; border-top:1px solid #e5edf5; color:#475569; }}
    </style>
</head>
<body>
<div class=\"container\">
    <div class=\"header\">
        <h1>Relatorio de Conversao</h1>
        <p>BrJoy WebP Optimizer • {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    </div>
    <div class=\"stats\">
        <div class=\"card\"><h3>Convertidos</h3><div class=\"value ok\">{success}</div><p>de {total} arquivos</p></div>
        <div class=\"card\"><h3>Erros</h3><div class=\"value err\">{errors}</div><p>{errors_percent:.1f}% falhas</p></div>
        <div class=\"card\"><h3>Economia Total</h3><div class=\"value save\">{total_saved/1024/1024:.1f} MB</div><p>{percent_saved:.1f}% reducao</p></div>
        <div class=\"card\"><h3>Tempo</h3><div class=\"value\">{int(duration//60)}:{int(duration%60):02d}</div><p>{avg_seconds:.2f}s por imagem</p></div>
    </div>
    <div class=\"section\">
        <h2>Top 10 - Maior Economia</h2>
        <table>
            <tr><th>Arquivo</th><th class=\"size\">Antes</th><th class=\"size\">Depois</th><th class=\"size\">Economia</th></tr>
"""

        for item in top_10:
            report_html += f"<tr><td>{html.escape(str(item['file']))}</td><td class='size'>{item['before']/1024:.1f} KB</td><td class='size'>{item['after']/1024:.1f} KB</td><td class='saving'>-{item['saved']/1024:.1f} KB ({item['percent']:.1f}%)</td></tr>"

        report_html += f"""
        </table>
    </div>
    <div class=\"footer\">
        <p><strong>Pasta(s) de origem ({len(resolved_source_folders)}):</strong></p>
        <ul class=\"paths\">{source_folders_html}</ul>
        <p><strong>Pasta(s) de saida ({len(output_folders)}):</strong></p>
        <ul class=\"paths\">{output_folders_html}</ul>
        <p><strong>Pasta de relatorios:</strong> {html.escape(str(report_folder))}</p>
    </div>
</div>
</body>
</html>
"""

        report_path = report_folder / "conversion-report.html"
        report_path.write_text(report_html, encoding="utf-8")

        metadata = {
            "id": report_folder.name,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "output_folder": str(output_folder),
            "report_folder": str(report_folder),
            "html_report": str(report_path),
            "ai_report": ai_paths["ai_report"],
            "csv_report": ai_paths["csv_report"],
            "source_folders": resolved_source_folders,
            "output_folders": output_folders,
            "success": success,
            "errors": errors,
            "total": total,
            "duration_seconds": round(duration, 2),
            "formato": formato,
        }
        self._store_report_metadata(metadata)
        return metadata

    def _generate_ai_report(self, report_folder: Path, details: list[dict[str, Any]], formato: str) -> dict[str, str]:
        first_original, first_converted = self._build_converted_report_path(details[0]["file"], formato)
        lines = [
            "# BrJoy WebP Optimizer - AI Code Update Report",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "#",
            "# INSTRUCOES PARA IA:",
            "# Substitua APENAS ANTES -> DEPOIS mantendo estrutura de pastas.",
            "",
            "# LISTA DE SUBSTITUICOES",
            "# ----------------------",
            "",
        ]

        for item in details:
            original_name, new_name = self._build_converted_report_path(item["file"], formato)
            lines.append(f"{original_name} -> {new_name}")

        lines.extend(
            [
                "",
                "# FORMATO CSV (para importar em planilhas)",
                "# ----------------------------------------",
                "",
                "ANTES,DEPOIS,ECONOMIA_KB,ECONOMIA_PERCENT",
            ]
        )

        for item in details:
            original_name, new_name = self._build_converted_report_path(item["file"], formato)
            lines.append(f"{original_name},{new_name},{item['saved']/1024:.1f},{item['percent']:.1f}")

        lines.extend(
            [
                "",
                "# EXEMPLOS DE SUBSTITUICAO NO CODIGO",
                "# HTML:",
                f"# <img src=\"images/{first_original}\" />",
                "# ↓",
                f"# <img src=\"images/{first_converted}\" />",
                "#",
                "# PROMPT SUGERIDO PARA IA:",
                "# \"Analise meu codigo e substitua somente os caminhos ANTES pelos DEPOIS, 1:1, sem alterar estrutura de pastas.\"",
            ]
        )

        ai_report_path = report_folder / "AI-CODE-UPDATE.txt"
        ai_report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        csv_path = report_folder / "conversions.csv"
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ANTES", "DEPOIS", "TAMANHO_ANTES_KB", "TAMANHO_DEPOIS_KB", "ECONOMIA_KB", "ECONOMIA_PERCENT"])
            for item in details:
                original_name, new_name = self._build_converted_report_path(item["file"], formato)
                writer.writerow(
                    [
                        self._safe_csv_cell(original_name),
                        self._safe_csv_cell(new_name),
                        f"{item['before']/1024:.1f}",
                        f"{item['after']/1024:.1f}",
                        f"{item['saved']/1024:.1f}",
                        f"{item['percent']:.1f}",
                    ]
                )

        return {
            "ai_report": str(ai_report_path),
            "csv_report": str(csv_path),
        }
