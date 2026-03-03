from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConversionItemStatus:
    id: str
    path: str
    relPath: str
    size: int
    sizeAfter: int = 0
    status: str = "pending"
    error: str = ""


@dataclass
class ConversionJob:
    id: str
    config: dict[str, Any]
    items: list[ConversionItemStatus]
    phase: str = "queued"
    completed: int = 0
    total: int = 0
    success: int = 0
    errors: int = 0
    skipped: int = 0
    message: str = ""
    startedAt: str = ""
    finishedAt: str = ""
    durationSeconds: float = 0.0
    reportId: str = ""
    outputFolder: str = ""
    sourceFolders: list[str] = field(default_factory=list)
    cancelRequested: bool = False
