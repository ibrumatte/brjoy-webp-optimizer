from __future__ import annotations

import uuid
from pathlib import Path

from app.core.constants import IGNORED_DIRS, MAX_SCAN_DEPTH, MAX_SCAN_FILES, SUPPORTED_EXTENSIONS


class ScanService:
    def scan_folder(self, root_path: str, extensions: list[str] | None = None) -> list[dict]:
        root = Path(root_path).expanduser().resolve()
        if not root.exists() or not root.is_dir():
            raise ValueError("Folder not found")
        allowed_extensions = self._normalize_extensions(extensions)

        found: list[dict] = []

        def scan_dir(path: Path, depth: int = 0) -> None:
            if depth > MAX_SCAN_DEPTH or len(found) >= MAX_SCAN_FILES:
                return
            try:
                entries = sorted(path.iterdir(), key=lambda p: p.name.lower())
            except (PermissionError, FileNotFoundError, NotADirectoryError):
                return

            for item in entries:
                if len(found) >= MAX_SCAN_FILES:
                    return
                if item.is_dir():
                    if item.name not in IGNORED_DIRS:
                        scan_dir(item, depth + 1)
                    continue
                if item.is_file() and item.suffix.lower() in allowed_extensions:
                    rel_path = item.relative_to(root)
                    found.append(self._to_file_item(item, rel_path))

        scan_dir(root)
        return found

    def collect_paths(self, paths: list[str], base_folder: str | None = None, extensions: list[str] | None = None) -> list[dict]:
        base = Path(base_folder).resolve() if base_folder else None
        allowed_extensions = self._normalize_extensions(extensions)
        found: dict[str, dict] = {}

        for raw in paths:
            path = Path(raw).expanduser()
            if not path.exists():
                continue

            if path.is_file() and path.suffix.lower() in allowed_extensions:
                item = self._to_file_item(path, self._resolve_rel(path, base))
                found[item["path"]] = item
                continue

            if path.is_dir():
                for file_item in self.scan_folder(str(path.resolve()), extensions=list(allowed_extensions)):
                    abs_path = str(Path(file_item["path"]).resolve())
                    if base:
                        rel = self._resolve_rel(Path(abs_path), base)
                        file_item["relPath"] = str(rel)
                    found[abs_path] = file_item

        return list(found.values())

    def _normalize_extensions(self, extensions: list[str] | None) -> set[str]:
        if not extensions:
            return set(SUPPORTED_EXTENSIONS)
        normalized: set[str] = set()
        for raw in extensions:
            value = str(raw or "").strip().lower()
            if not value:
                continue
            ext = value if value.startswith(".") else f".{value}"
            if ext in SUPPORTED_EXTENSIONS:
                normalized.add(ext)
        return normalized or set(SUPPORTED_EXTENSIONS)

    def _resolve_rel(self, path: Path, base: Path | None):
        resolved = path.resolve()
        if not base:
            return resolved.name
        try:
            return resolved.relative_to(base)
        except ValueError:
            return resolved.name

    def _to_file_item(self, path: Path, rel_path) -> dict:
        resolved = path.resolve()
        return {
            "id": str(uuid.uuid4()),
            "path": str(resolved),
            "relPath": str(rel_path),
            "size": resolved.stat().st_size,
            "sizeAfter": 0,
            "status": "pending",
        }
