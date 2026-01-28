# src/Inspection/application/services/diagnosis_services.py
from __future__ import annotations

import os
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
    Implementación limpia del Port para la UX nueva.

    Cambios clave:
      - No expone list_models/select_model a la UI.
      - Modelo fijo desde config (vision.model_id).
      - Un solo botón Start/Stop -> toggle_diagnosis().
      - Sesiones visibles son SOLO del registry local (sin UUID).
      - Summary valida si ya existe PDF para no regenerar.
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
        self._registry = diagnosis_sessions_registry

        self._model_id_cfg = (model_id_from_config or "").strip()
        self._active_model_id: Optional[str] = None

        self._operator_ctx: Optional[DiagnosisOperatorContext] = None

        self._state = "IDLE"      # IDLE | RUNNING | STOPPED
        self._initialized = False

        self._current_session_id: Optional[str] = None
        self._current_entry_key: Optional[str] = None
        self._current_entry_label: Optional[str] = None

        # Carpeta donde el sistema 2 deja artifacts del reporte (pdf esperado)
        self._report_artifacts_dir = report_artifacts_dir

    # -------------------------
    # Estado / getters
    # -------------------------
    def get_state(self) -> str:
        return self._state

    def get_active_model_id(self) -> Optional[str]:
        return self._active_model_id

    def set_operator_context(self, operator: str, location: str, job_order: str) -> None:
        self._operator_ctx = DiagnosisOperatorContext(
            operator=(operator or "").strip(),
            location=(location or "").strip(),
            job_order=(job_order or "").strip(),
        )

    def get_operator_context(self) -> Optional[DiagnosisOperatorContext]:
        return self._operator_ctx

    def get_current_display_label(self) -> Optional[str]:
        return self._current_entry_label

    # -------------------------
    # 1) Initialize Vision System
    # -------------------------
    def initialize_vision_system(self) -> Dict[str, Any]:
        """
        Selecciona modelo fijo desde config, sin exponer combos a la UI.
        """
        if self._state == "RUNNING":
            return {"ok": False, "error": "No se puede inicializar mientras el diagnóstico está en ejecución."}

        try:
            if not self._model_id_cfg:
                return {"ok": False, "error": "Falta vision.model_id en el archivo de configuración."}

            models = self._controller.list_models()
            resolved_id = self._resolve_model_id(models=models, wanted=self._model_id_cfg)
            if not resolved_id:
                return {"ok": False, "error": f"No se pudo resolver el modelo desde config: {self._model_id_cfg!r}"}

            # Selecciona SIEMPRE el modelo de config (operadores no eligen modelo)
            self._controller.select_model(resolved_id)

            # El endpoint solo da bool, validamos que al menos quede activo
            if not self._controller.has_active_model():
                return {"ok": False, "error": "El sistema de visión no reporta un modelo activo luego de seleccionar."}

            self._active_model_id = resolved_id
            self._initialized = True
            self._state = "IDLE"
            self._current_session_id = None
            self._current_entry_key = None
            self._current_entry_label = None

            return {
                "ok": True,
                "active_model_id": self._active_model_id,
                "message": "Vision system initialized successfully.",
            }

        except Exception as exc:
            self._logger.error("initialize_vision_system failed: %s", exc, exc_info=True)
            return {"ok": False, "error": str(exc)}

    # -------------------------
    # 2) Toggle Diagnosis (Start/Stop en un botón)
    # -------------------------
    def toggle_diagnosis(self) -> Dict[str, Any]:
        # Validaciones base
        if not self._initialized:
            return {"ok": False, "error": "Vision system is not initialized. Press 'Start Diagnosis Session' again."}

        if self._operator_ctx is None:
            return {"ok": False, "error": "Faltan datos: Operator/Location/Job Order (se piden al inicializar)."}

        # Si está corriendo -> STOP
        if self._state == "RUNNING":
            return self._stop_internal()

        # Si NO está corriendo -> START
        return self._start_internal()

    def _ensure_model_active(self) -> Optional[str]:
        """
        En caso de que el sistema 2 haya reiniciado y perdió modelo activo.
        """
        if self._controller.has_active_model():
            return self._active_model_id or self._model_id_cfg

        models = self._controller.list_models()
        resolved_id = self._resolve_model_id(models=models, wanted=self._model_id_cfg)
        if not resolved_id:
            return None

        self._controller.select_model(resolved_id)
        if not self._controller.has_active_model():
            return None

        self._active_model_id = resolved_id
        return resolved_id

    def _start_internal(self) -> Dict[str, Any]:
        try:
            model_id = self._ensure_model_active()
            if not model_id:
                return {"ok": False, "error": f"No se pudo activar el modelo requerido: {self._model_id_cfg!r}"}

            session_id = str(self._controller.start_video_session())
            self._current_session_id = session_id

            # Conectar WS (no bloqueante; corre en thread del adapter)
            self._controller.connect_report_ws(session_id)

            # Crear y registrar entry local (sin UUID visible)
            entry: DiagnosisSessionEntry = self._registry.create_entry(
                session_id=session_id,
                operator=self._operator_ctx.operator,
                location=self._operator_ctx.location,
                job_order=self._operator_ctx.job_order,
                model_id=model_id,
                when=datetime.now(),
            )
            self._registry.upsert(entry)

            self._current_entry_key = entry.display_key
            self._current_entry_label = entry.display_label

            self._state = "RUNNING"
            return {
                "ok": True,
                "action": "started",
                "state": self._state,
                "display_key": entry.display_key,
                "display_label": entry.display_label,
            }

        except Exception as exc:
            self._logger.error("start diagnosis failed: %s", exc, exc_info=True)
            return {"ok": False, "error": str(exc)}

    def _stop_internal(self) -> Dict[str, Any]:
        try:
            sid = self._current_session_id
            # Si por alguna razón no hay sid, igual marcamos STOPPED
            if not sid:
                self._state = "STOPPED"
                self._controller.disconnect_report_ws()
                return {"ok": True, "action": "stopped", "state": self._state}

            status = self._controller.stop_video_session(sid)
            try:
                self._controller.disconnect_report_ws()
            finally:
                self._current_session_id = None
                self._state = "STOPPED"

            return {"ok": True, "action": "stopped", "state": self._state, "status": status}

        except Exception as exc:
            self._logger.error("stop diagnosis failed: %s", exc, exc_info=True)
            return {"ok": False, "error": str(exc)}

    # -------------------------
    # 5) Lista de sesiones registradas (buscable)
    # -------------------------
    def list_registered_sessions(self, query: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        items = self._registry.search(query=query, limit=limit) if (query or "").strip() else self._registry.list_recent(limit=limit)

        # Devuelve dicts listos para UI
        out: List[Dict[str, Any]] = []
        for e in items:
            out.append({
                "display_key": e.display_key,
                "display_label": e.display_label,
                "session_id": e.session_id,  # interno (no mostrar)
                "created_at": e.created_at.isoformat(),
                "operator": e.operator,
                "location": e.location,
                "job_order": e.job_order,
                "model_id": e.model_id,
                "summary_generated": bool(e.summary_generated),
                "summary_pdf_path": e.summary_pdf_path,
            })
        return out

    # -------------------------
    # 6) Summary report con validación (no regenerar)
    # -------------------------
    def get_summary_report(self, display_key: str, force: bool = False) -> Dict[str, Any]:
        if self._state == "RUNNING":
            return {"ok": False, "error": "Detén el diagnóstico antes de generar el reporte."}

        entry = self._registry.get(display_key)
        if entry is None:
            return {"ok": False, "error": "No se encontró la sesión seleccionada en el registro local."}

        # Determinar ruta esperada del PDF (si se conoce carpeta artifacts)
        expected_pdf = None
        if self._report_artifacts_dir:
            expected_pdf = os.path.join(self._report_artifacts_dir, f"{entry.session_id}_report", "report.pdf")

        # Si ya estaba marcado como generado, y existe PDF, no regenerar
        if not force:
            if entry.summary_pdf_path and os.path.exists(entry.summary_pdf_path):
                return {
                    "ok": True,
                    "already_generated": True,
                    "pdf_path": entry.summary_pdf_path,
                    "summary": None,
                }
            if expected_pdf and os.path.exists(expected_pdf):
                # Auto-curación: si el pdf existe pero no estaba registrado
                entry.summary_generated = True
                entry.summary_generated_at = datetime.now()
                entry.summary_pdf_path = expected_pdf
                self._registry.upsert(entry)
                return {
                    "ok": True,
                    "already_generated": True,
                    "pdf_path": expected_pdf,
                    "summary": None,
                }

        # Si hay que generar, llamamos al endpoint summary
        try:
            summary = self._controller.get_report_summary(
                session_id=entry.session_id,
                operator=entry.operator,
                location=entry.location,
                job_order=entry.job_order,
            )

            # Guardar path final (si existe). Si no existe aún, igual guardamos expected para que el operador lo busque.
            pdf_path = entry.summary_pdf_path
            if not pdf_path:
                pdf_path = expected_pdf

            entry.summary_generated = True
            entry.summary_generated_at = datetime.now()
            entry.summary_pdf_path = pdf_path
            self._registry.upsert(entry)

            return {
                "ok": True,
                "already_generated": False,
                "pdf_path": pdf_path,
                "summary": summary,
            }

        except Exception as exc:
            self._logger.error("get_summary_report failed: %s", exc, exc_info=True)
            return {"ok": False, "error": str(exc)}

    # -------------------------
    # Utils
    # -------------------------
    @staticmethod
    def _resolve_model_id(models: List[Dict[str, Any]], wanted: str) -> Optional[str]:
        """
        Intenta mapear el 'wanted' del config contra list_models() del sistema 2.
        Soporta variaciones típicas:
          - {"id": "...", "name": "..."}
          - {"model_id": "...", "name": "..."}
        """
        w = (wanted or "").strip()
        if not w:
            return None

        # Si no hay lista, asumimos que el id existe (dejar al server validar)
        if not models:
            return w

        # match exact por id/model_id
        for m in models:
            mid = m.get("model_id") or m.get("id")
            if mid is not None and str(mid).strip() == w:
                return str(mid).strip()

        # match por nombre
        for m in models:
            name = m.get("name") or m.get("model_name")
            mid = m.get("model_id") or m.get("id")
            if name is not None and str(name).strip() == w:
                return str(mid).strip() if mid is not None else str(name).strip()

        # fallback: usar lo del config
        return w
