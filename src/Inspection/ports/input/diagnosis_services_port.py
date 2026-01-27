# src/Inspection/ports/input/diagnosis_services_port.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from Inspection.application.dto.diagnosis_operator_context import DiagnosisOperatorContext


class DiagnosisServicesPort(ABC):
    """
    Port limpio alineado a la UX nueva (operador no técnico).

    UI (4 elementos):
      1) Initialize Vision System
      2) Start/Stop Diagnosis (mismo botón -> toggle)
      3) Lista de sesiones registradas (buscable, sin UUID visible)
      4) Get Summary Report (valida si ya existe)

    Convenciones de retorno (Dict):
      - Siempre que sea posible, retorna {"ok": bool, ...}
      - Errores: {"ok": False, "error": "..."}
    """

    # -------------------------
    # 1) Inicialización / Modelo fijo
    # -------------------------
    @abstractmethod
    def initialize_vision_system(self) -> Dict[str, Any]:
        """
        - Verifica que el sistema 2 responde (list_models/has_active_model)
        - Resuelve el modelo de config y lo selecciona
        - Deja el servicio en estado inicializado
        Retorna:
          {"ok": True, "active_model_id": "...", "message": "..."}
          o {"ok": False, "error": "..."}
        """
        raise NotImplementedError

    @abstractmethod
    def get_active_model_id(self) -> Optional[str]:
        """Modelo activo (resuelto desde config)."""
        raise NotImplementedError

    # -------------------------
    # 1.d) Contexto del operador (para Summary)
    # -------------------------
    @abstractmethod
    def set_operator_context(self, operator: str, location: str, job_order: str) -> None:
        """Guardar Operator/Location/JobOrder (se piden vía diálogo en Initialize)."""
        raise NotImplementedError

    @abstractmethod
    def get_operator_context(self) -> Optional[DiagnosisOperatorContext]:
        raise NotImplementedError

    # -------------------------
    # 2) Start/Stop (toggle)
    # -------------------------
    @abstractmethod
    def toggle_diagnosis(self) -> Dict[str, Any]:
        """
        Si está STOPPED/IDLE -> START:
          - start_video_session()
          - connect_report_ws(session_id)
          - registra sesión en registry local con display_label humano
        Si está RUNNING -> STOP:
          - stop_video_session(session_id)
          - disconnect_report_ws()

        Retorna (ejemplos):
          START:
            {"ok": True, "action": "started", "state": "RUNNING",
             "display_key": "...", "display_label": "..."}
          STOP:
            {"ok": True, "action": "stopped", "state": "STOPPED"}
          ERROR:
            {"ok": False, "error": "..."}
        """
        raise NotImplementedError

    @abstractmethod
    def get_state(self) -> str:
        """IDLE | RUNNING | STOPPED"""
        raise NotImplementedError

    @abstractmethod
    def get_current_display_label(self) -> Optional[str]:
        """Label humano de la sesión actual (para overlay, sin UUID)."""
        raise NotImplementedError

    # -------------------------
    # 5) Sesiones registradas (buscables, últimas 20)
    # -------------------------
    @abstractmethod
    def list_registered_sessions(self, query: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """
        Devuelve items listos para poblar QComboBox/QList:
          [
            {
              "display_key": "...",     # interno
              "display_label": "...",   # visible para operador
              "session_id": "...",      # interno (NO mostrar)
              "created_at": "...",      # ISO string
              "operator": "...",
              "location": "...",
              "job_order": "...",
              "model_id": "...",
              "summary_generated": bool,
              "summary_pdf_path": str|None,
            },
            ...
          ]
        """
        raise NotImplementedError

    # -------------------------
    # 6) Summary report (valida si ya existe)
    # -------------------------
    @abstractmethod
    def get_summary_report(self, display_key: str, force: bool = False) -> Dict[str, Any]:
        """
        - Solo permitido si NO está RUNNING
        - Busca entry en registry por display_key
        - Si summary ya generado y existe PDF (o force=False) -> no regenerar
        - Si no existe -> llama /report/summary/{session_id} usando operator/location/job_order guardados

        Retorna:
          {"ok": True, "already_generated": bool, "pdf_path": "...", "summary": {...}}
          o {"ok": False, "error": "..."}
        """
        raise NotImplementedError
