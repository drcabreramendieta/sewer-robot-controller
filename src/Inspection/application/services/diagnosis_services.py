from typing import Any, Dict, List, Optional
from logging import Logger

from Inspection.ports.input import DiagnosisServicesPort
from Inspection.ports.output import DiagnosisControllerPort

class DiagnosisServices(DiagnosisServicesPort):
    def __init__(
        self,
        controller: DiagnosisControllerPort,
        logger: Logger,
    ) -> None:
        super().__init__()
        self._controller = controller
        self._logger = logger
        self._state = "IDLE"  # IDLE | RUNNING | STOPPED


        self._current_session_id: Optional[str] = None

    def get_current_session_id(self) -> Optional[str]:
        return self._current_session_id
    
    def get_state(self) -> str:
        return self._state

    def initialize_system(self) -> Dict[str, Any]:
        """
        Modo recomendado:
        - NO intenta arrancar procesos remotos.
        - Solo valida conectividad y precarga listas para la UI.
        """
        try:
            has_model = self._controller.has_active_model()
            models = self._controller.list_models()
            sessions = self._controller.list_report_sessions()

            # Bloquear initialize si RUNNING
            if self._state == "RUNNING":
                msg = "No se puede inicializar mientras el diagnóstico está en ejecución. Detén la sesión primero."
                return {"ok": False, "error": msg, "models": [], "sessions": []}

            return {"ok": True, "has_active_model": has_model, "models": models, "sessions": sessions}
        except Exception as exc:
            self._logger.error("Vision initialize_system failed: %s", exc, exc_info=True)
            return {"ok": False, "error": str(exc), "models": [], "sessions": []}

    def list_models(self) -> List[Dict[str, Any]]:
        return self._controller.list_models()

    def select_model(self, model_id: str) -> Dict[str, Any]:
        resp = self._controller.select_model(model_id)
        return resp

    def list_sessions(self) -> List[str]:
        return self._controller.list_report_sessions()

    def start_diagnosis_session(self, operator: str, location: str, job_order: Optional[str] = None) -> str:
        # Bloquear start si ya está RUNNING
        if self._state == "RUNNING":
            msg = "Ya hay una sesión de diagnóstico en ejecución. Detén la sesión actual antes de iniciar otra."
            raise RuntimeError(msg)
 
        # Validación mínima: que haya modelo activo
        if not self._controller.has_active_model():
            msg = "No se puede iniciar diagnóstico: no hay modelo activo. Selecciona un modelo primero."
            raise RuntimeError(msg)

        # Si ya hay sesión activa, la detenemos primero (por seguridad)
        if self._current_session_id is not None:
            try:
                self.stop_diagnosis_session()
            except Exception:
                pass

        session_id = self._controller.start_video_session()
        self._current_session_id = session_id
        self._state = "RUNNING"

        # Conexión WS (no bloqueante: el adapter debe correr en hilo)
        self._controller.connect_report_ws(session_id)

        return session_id

    def stop_diagnosis_session(self) -> str:
        if self._current_session_id is None:
            return "no-active-session"

        sid = self._current_session_id

        # 1) detener video session en API
        status = self._controller.stop_video_session(sid)

        # 2) cortar WS
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
        # summary solo si STOPPED
        if self._state != "STOPPED":
            msg = "No se puede pedir el reporte/summary mientras el diagnóstico esté en ejecución. Detén el diagnóstico primero."
            raise RuntimeError(msg)

        summary = self._controller.get_report_summary(session_id, operator, location, job_order)
        return summary
