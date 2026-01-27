from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from logging import Logger
from typing import Any, Dict, List, Optional

from Inspection.application.dto.diagnosis_operator_context import DiagnosisOperatorContext
from Inspection.application.services.diagnosis_sessions_registry import (
    DiagnosisSessionsRegistry,
    DiagnosisSessionEntry,
)
from Inspection.ports.input import DiagnosisServicesPort
from Inspection.ports.output import DiagnosisControllerPort


class DiagnosisServices(DiagnosisServicesPort):
    """
    Implementa DiagnosisServicesPort (interfaz estable).
    Internamente soporta la nueva UX (modelo desde config, sesiones con display_key, etc.)
    """

    def __init__(
        self,
        controller: DiagnosisControllerPort,
        logger: Logger,
        model_id_from_config: str,
        diagnosis_sessions_registry: DiagnosisSessionsRegistry,
        report_artifacts_dir: Optional[str] = None,
    ) -> None:
        super().__init__()
        self._controller = controller
        self._logger = logger
        self.diagnosis_sessions_registry = diagnosis_sessions_registry

        self._state = "IDLE"  # IDLE | RUNNING | STOPPED
        self._initialized: bool = False

        self._operator_ctx: Optional[DiagnosisOperatorContext] = None

        self._model_id_cfg = model_id_from_config
        self._active_model_id: Optional[str] = None

        self._current_session_id: Optional[str] = None
        self._current_display_key: Optional[str] = None

        self._report_artifacts_dir = report_artifacts_dir

    # -------------------------
    # Helpers / estado
    # -------------------------
    def get_state(self) -> str:
        return self._state

    def is_initialized(self) -> bool:
        return self._initialized

    def get_current_session_id(self) -> Optional[str]:
        return self._current_session_id

    def get_current_display_key(self) -> Optional[str]:
        return self._current_display_key

    def get_operator_context(self) -> Optional[DiagnosisOperatorContext]:
        return self._operator_ctx

    # ============================================================
    # ✅ Implementación requerida por DiagnosisServicesPort (ABSTRACT)
    # ============================================================

    def initialize_system(self) -> Dict[str, Any]:
        """
        Compatibilidad con el Port viejo: health-check y precarga.
        En la nueva UX NO vas a poblar combos aquí, pero el Port lo exige.
        Retornamos info mínima sin romper.
        """
        if self._state == "RUNNING":
            return {"ok": False, "error": "No se puede inicializar mientras RUNNING."}

        try:
            models = self._controller.list_models()
            has_model = self._controller.has_active_model()
            sessions = self._controller.list_report_sessions()

            return {
                "ok": True,
                "has_active_model": has_model,
                "models": models,
                "sessions": sessions,
            }
        except Exception as exc:
            self._logger.error("initialize_system failed: %s", exc, exc_info=True)
            return {"ok": False, "error": str(exc), "models": [], "sessions": []}

    def list_models(self) -> List[Dict[str, Any]]:
        return self._controller.list_models()

    def select_model(self, model_id: str) -> Dict[str, Any]:
        return self._controller.select_model(model_id)

    def list_sessions(self) -> List[str]:
        # Port viejo devuelve UUIDs del sistema 2.
        return self._controller.list_report_sessions()

    def start_diagnosis_session(
        self,
        operator: str,
        location: str,
        job_order: Optional[str] = None,
    ) -> str:
        """
        Port viejo: hace TODO y devuelve UUID.
        Lo adaptamos a tu lógica nueva:
        - guarda operator ctx
        - asegura modelo activo (selecciona desde config si hace falta)
        - start + connect WS
        - crea entry en registry con display_key
        """
        job_order = job_order or ""

        # Si no inicializaste por la UX nueva, igual guardamos ctx aquí
        if self._operator_ctx is None:
            self._operator_ctx = DiagnosisOperatorContext(operator=operator, location=location, job_order=job_order)

        # Bloquear start si ya está RUNNING
        if self._state == "RUNNING":
            raise RuntimeError("Ya hay una sesión de diagnóstico en ejecución. Detén la sesión actual antes de iniciar otra.")

        # Asegurar modelo activo
        if not self._controller.has_active_model():
            # intentamos seleccionar el modelo desde config (modo UX nueva)
            models = self._controller.list_models()
            resolved_id = self._resolve_model_id(models=models, wanted=self._model_id_cfg)
            if not resolved_id:
                raise RuntimeError(f"No se encontró el modelo indicado en config: {self._model_id_cfg!r}")
            self._controller.select_model(resolved_id)

            if not self._controller.has_active_model():
                raise RuntimeError("No hay modelo activo en el sistema de visión. Revisa MLflow/selección de modelo.")

            self._active_model_id = resolved_id

        session_id = str(self._controller.start_video_session())
        self._current_session_id = session_id
        self._state = "RUNNING"

        # WS (no bloqueante)
        self._controller.connect_report_ws(session_id)

        # Registry local con display_key
        display_key = self._sessions_registry.build_display_key(
            operator=self._operator_ctx.operator,
            location=self._operator_ctx.location,
            job_order=self._operator_ctx.job_order,
            when=datetime.now(),
        )
        self._current_display_key = display_key

        entry = DiagnosisSessionEntry(
            display_key=display_key,
            session_id=session_id,
            operator=self._operator_ctx.operator,
            location=self._operator_ctx.location,
            job_order=self._operator_ctx.job_order,
            model_id=self._active_model_id or self._model_id_cfg,
            created_at=datetime.now(),
            summary_generated=False,
            summary_generated_at=None,
            summary_pdf_path=None,
        )
        self._sessions_registry.upsert(entry)

        # ✅ Port pide STR
        return session_id

    def stop_diagnosis_session(self) -> str:
        if self._current_session_id is None:
            self._state = "STOPPED"
            return "no-active-session"

        sid = self._current_session_id
        status = self._controller.stop_video_session(sid)

        try:
            self._controller.disconnect_report_ws()
        finally:
            self._current_session_id = None
            self._state = "STOPPED"

        return status

    def get_summary(
        self,
        session_id: str,
        operator: str,
        location: str,
        job_order: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Port viejo: summary por UUID + datos.
        Mantiene la regla: solo si STOPPED.
        """
        if self._state == "RUNNING":
            raise RuntimeError("No se puede pedir el reporte/summary mientras el diagnóstico esté en ejecución. Detén el diagnóstico primero.")

        return self._controller.get_report_summary(
            session_id=session_id,
            operator=operator,
            location=location,
            job_order=job_order,
        )

    # ============================================================
    # ✅ Métodos nuevos (UX nueva)
    # ============================================================

    def initialize_vision_system(self, operator: str, location: str, job_order: str) -> Dict[str, Any]:
        """
        Método nuevo (UX nueva): setea modelo desde config y guarda context.
        """
        if self._state == "RUNNING":
            return {"ok": False, "error": "No se puede inicializar mientras el diagnóstico está en ejecución."}

        try:
            self._operator_ctx = DiagnosisOperatorContext(operator=operator, location=location, job_order=job_order)

            models = self._controller.list_models()
            resolved_id = self._resolve_model_id(models=models, wanted=self._model_id_cfg)

            if not resolved_id:
                return {"ok": False, "error": f"No se encontró el modelo indicado en config: {self._model_id_cfg!r}"}

            self._controller.select_model(resolved_id)

            if not self._controller.has_active_model():
                return {"ok": False, "error": "El sistema de visión no reporta un modelo activo luego de seleccionar."}

            self._active_model_id = resolved_id
            self._initialized = True
            self._state = "IDLE"
            self._current_session_id = None
            self._current_display_key = None

            return {"ok": True, "active_model_id": self._active_model_id, "operator_ctx": asdict(self._operator_ctx)}

        except Exception as exc:
            self._logger.error("initialize_vision_system failed: %s", exc, exc_info=True)
            return {"ok": False, "error": str(exc)}

    def list_recent_sessions(self, limit: int = 20) -> List[str]:
        entries = self._sessions_registry.list_recent(limit=limit)
        return [e.display_key for e in entries]

    def search_sessions(self, query: str, limit: int = 20) -> List[str]:
        entries = self._sessions_registry.search(query=query, limit=limit)
        return [e.display_key for e in entries]

    def get_summary_by_display_key(self, display_key: str, force: bool = False) -> Dict[str, Any]:
        if self._state == "RUNNING":
            raise RuntimeError("Detén el diagnóstico antes de generar el reporte.")

        entry = self._sessions_registry.get(display_key)
        if entry is None:
            raise RuntimeError("No se encontró la sesión seleccionada en el registry local.")

        if entry.summary_generated and not force:
            return {
                "ok": False,
                "already_generated": True,
                "display_key": entry.display_key,
                "session_id": entry.session_id,
                "pdf_path": entry.summary_pdf_path,
                "message": "El reporte de esta sesión ya fue generado previamente.",
            }

        summary = self._controller.get_report_summary(
            session_id=entry.session_id,
            operator=entry.operator,
            location=entry.location,
            job_order=entry.job_order,
        )

        pdf_path = entry.summary_pdf_path
        if not pdf_path and self._report_artifacts_dir:
            pdf_path = f"{self._report_artifacts_dir}/{entry.session_id}_report/report.pdf"

        entry.summary_generated = True
        entry.summary_generated_at = datetime.now()
        entry.summary_pdf_path = pdf_path
        self._sessions_registry.upsert(entry)

        return {"ok": True, "display_key": entry.display_key, "session_id": entry.session_id, "pdf_path": pdf_path, "summary": summary}

    # -------------------------
    # Utils
    # -------------------------
    @staticmethod
    def _resolve_model_id(models: List[Dict[str, Any]], wanted: str) -> Optional[str]:
        if not wanted:
            return None

        w = str(wanted).strip()
        if not models:
            return w

        for m in models:
            mid = m.get("model_id") or m.get("id")
            name = m.get("name") or m.get("model_name")
            if mid is not None and str(mid) == w:
                return str(mid)
            if name is not None and str(name) == w:
                return str(mid) if mid is not None else str(name)

        return w
