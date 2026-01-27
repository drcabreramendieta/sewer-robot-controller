from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class DiagnosisSessionEntry:
    display_key: str
    session_id: str
    operator: str
    location: str
    job_order: str
    model_id: str
    created_at: datetime

    summary_generated: bool
    summary_generated_at: Optional[datetime]
    summary_pdf_path: Optional[str]


class DiagnosisSessionsRegistry:
    def __init__(self, path: str) -> None:
        self._path = path
        self._entries: dict[str, DiagnosisSessionEntry] = {}
        self._load()

    def build_display_key(self, operator: str, location: str, job_order: str, when: datetime) -> str:
        def norm(s: str) -> str:
            return (s or "").strip().replace(" ", "_")
        ts = when.strftime("%Y-%m-%d_%H%M%S")
        return f"{norm(operator)}__{norm(location)}__{norm(job_order)}__{ts}"

    def upsert(self, entry: DiagnosisSessionEntry) -> None:
        self._entries[entry.display_key] = entry
        self._save()

    def get(self, display_key: str) -> Optional[DiagnosisSessionEntry]:
        return self._entries.get(display_key)

    def list_recent(self, limit: int = 20) -> List[DiagnosisSessionEntry]:
        items = sorted(self._entries.values(), key=lambda e: e.created_at, reverse=True)
        return items[: max(0, limit)]

    def search(self, query: str, limit: int = 20) -> List[DiagnosisSessionEntry]:
        q = (query or "").strip().lower()
        items = self.list_recent(limit=10_000)
        if not q:
            return items[: max(0, limit)]
        filtered = [e for e in items if q in e.display_key.lower()]
        return filtered[: max(0, limit)]

    # -------------------
    # Persistencia
    # -------------------
    def _load(self) -> None:
        if not os.path.exists(self._path):
            return
        with open(self._path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for dk, data in raw.items():
            self._entries[dk] = DiagnosisSessionEntry(
                display_key=data["display_key"],
                session_id=data["session_id"],
                operator=data["operator"],
                location=data["location"],
                job_order=data["job_order"],
                model_id=data["model_id"],
                created_at=datetime.fromisoformat(data["created_at"]),
                summary_generated=bool(data.get("summary_generated", False)),
                summary_generated_at=datetime.fromisoformat(data["summary_generated_at"])
                if data.get("summary_generated_at")
                else None,
                summary_pdf_path=data.get("summary_pdf_path"),
            )

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
        raw = {}
        for dk, e in self._entries.items():
            d = asdict(e)
            d["created_at"] = e.created_at.isoformat()
            d["summary_generated_at"] = e.summary_generated_at.isoformat() if e.summary_generated_at else None
            raw[dk] = d
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
