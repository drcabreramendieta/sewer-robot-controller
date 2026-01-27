# src/Inspection/application/services/diagnosis_sessions_registry.py
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class DiagnosisSessionEntry:
    # Interno (clave única)
    display_key: str

    # Visible al operador (humano y buscable)
    display_label: str

    # Interno: UUID del sistema 2 (NO mostrar)
    session_id: str

    # Metadata necesaria para Summary
    operator: str
    location: str
    job_order: str

    # Requisito: guardar modelo usado (mlflow/model_id)
    model_id: str

    created_at: datetime

    # Control de reportes
    summary_generated: bool
    summary_generated_at: Optional[datetime]
    summary_pdf_path: Optional[str]


class DiagnosisSessionsRegistry:
    """
    Registro local (Sistema 1) para mapear:
      display_key (interno) -> session_id (uuid interno) + metadata.

    UX:
      - display_label NO muestra UUID
      - búsqueda por substring (fecha, operador, location, job order)
      - últimas N (default 20)
    """

    def __init__(self, path: str) -> None:
        self._path = path
        self._entries: dict[str, DiagnosisSessionEntry] = {}
        self._load()

    # -------------------------
    # Construcción de claves/labels
    # -------------------------
    def build_display_key(self, operator: str, location: str, job_order: str, when: datetime) -> str:
        """
        Clave interna (estable, sin espacios) para evitar problemas de persistencia.
        """
        def norm(s: str) -> str:
            return (s or "").strip().replace(" ", "_")

        ts = when.strftime("%Y-%m-%d_%H%M%S")
        return f"{norm(operator)}__{norm(location)}__{norm(job_order)}__{ts}"

    def build_display_label(self, operator: str, location: str, job_order: str, when: datetime) -> str:
        """
        Label visible al operador, fácil de leer/buscar.
        """
        ts = when.strftime("%Y-%m-%d %H:%M:%S")
        op = (operator or "").strip() or "N/A"
        loc = (location or "").strip() or "N/A"
        jo = (job_order or "").strip() or "N/A"
        return f"{ts} | {op} | {loc} | {jo}"

    def create_entry(
        self,
        session_id: str,
        operator: str,
        location: str,
        job_order: str,
        model_id: str,
        when: Optional[datetime] = None,
    ) -> DiagnosisSessionEntry:
        """
        Crea un entry garantizando display_key único (si hay colisión, agrega sufijo).
        """
        when = when or datetime.now()
        base_key = self.build_display_key(operator, location, job_order, when)
        display_key = base_key
        i = 2
        while display_key in self._entries:
            display_key = f"{base_key}__{i}"
            i += 1

        display_label = self.build_display_label(operator, location, job_order, when)

        return DiagnosisSessionEntry(
            display_key=display_key,
            display_label=display_label,
            session_id=session_id,
            operator=operator,
            location=location,
            job_order=job_order,
            model_id=model_id,
            created_at=when,
            summary_generated=False,
            summary_generated_at=None,
            summary_pdf_path=None,
        )

    # -------------------------
    # API pública
    # -------------------------
    def upsert(self, entry: DiagnosisSessionEntry) -> None:
        self._entries[entry.display_key] = entry
        self._save()

    def get(self, display_key: str) -> Optional[DiagnosisSessionEntry]:
        return self._entries.get(display_key)

    def list_recent(self, limit: int = 20) -> List[DiagnosisSessionEntry]:
        items = sorted(self._entries.values(), key=lambda e: e.created_at, reverse=True)
        return items[: max(0, limit)]

    def search(self, query: str, limit: int = 20) -> List[DiagnosisSessionEntry]:
        """
        Búsqueda por substring sobre:
          - display_label (incluye fecha)
          - operator/location/job_order
          - model_id
        """
        q = (query or "").strip().lower()
        items = self.list_recent(limit=10_000)
        if not q:
            return items[: max(0, limit)]

        def haystack(e: DiagnosisSessionEntry) -> str:
            # display_label ya incluye fecha, así que sirve para buscar "2026-01-26", etc.
            return " | ".join([
                (e.display_label or ""),
                (e.operator or ""),
                (e.location or ""),
                (e.job_order or ""),
                (e.model_id or ""),
            ]).lower()

        filtered = [e for e in items if q in haystack(e)]
        return filtered[: max(0, limit)]

    # -------------------------
    # Persistencia
    # -------------------------
    def _load(self) -> None:
        if not self._path:
            return
        if not os.path.exists(self._path):
            return

        with open(self._path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        for dk, data in raw.items():
            created_at = datetime.fromisoformat(data["created_at"])

            # Compat: si un registry viejo no tiene display_label, lo reconstruimos
            display_label = data.get("display_label")
            if not display_label:
                display_label = self.build_display_label(
                    data.get("operator", ""),
                    data.get("location", ""),
                    data.get("job_order", ""),
                    created_at,
                )

            self._entries[dk] = DiagnosisSessionEntry(
                display_key=data["display_key"],
                display_label=display_label,
                session_id=data["session_id"],
                operator=data.get("operator", ""),
                location=data.get("location", ""),
                job_order=data.get("job_order", ""),
                model_id=data.get("model_id", ""),
                created_at=created_at,
                summary_generated=bool(data.get("summary_generated", False)),
                summary_generated_at=datetime.fromisoformat(data["summary_generated_at"])
                if data.get("summary_generated_at")
                else None,
                summary_pdf_path=data.get("summary_pdf_path"),
            )

    def _save(self) -> None:
        if not self._path:
            return

        os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)

        raw = {}
        for dk, e in self._entries.items():
            d = asdict(e)
            d["created_at"] = e.created_at.isoformat()
            d["summary_generated_at"] = e.summary_generated_at.isoformat() if e.summary_generated_at else None
            raw[dk] = d

        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
