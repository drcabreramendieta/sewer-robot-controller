from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class DiagnosisControllerPort(ABC):
    """Puerto de salida: cliente hacia el sistema de visión (FastAPI + WS)."""

    @abstractmethod
    def list_models(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def select_model(self, model_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def has_active_model(self) -> bool:
        pass

    @abstractmethod
    def start_video_session(self) -> str:
        """Retorna session_id (UUID como string)."""
        pass

    @abstractmethod
    def stop_video_session(self, session_id: str) -> str:
        pass

    @abstractmethod
    def get_video_status(self, session_id: str) -> str:
        pass

    @abstractmethod
    def list_report_sessions(self) -> List[str]:
        pass

    @abstractmethod
    def get_report_summary(
        self,
        session_id: str,
        operator: str,
        location: str,
        job_order: Optional[str] = None,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def connect_report_ws(
        self,
        session_id: str,
    ) -> None:
        """Abre WS y publica payloads según el adapter."""
        pass

    @abstractmethod
    def disconnect_report_ws(self) -> None:
        pass

# Para revisar que los sistemas estén arriba en la jetson - no es crítico
#    @abstractmethod
#    def healthcheck(self) -> Dict[str, Any]:
#        """Debe ser rápido: valida que FastAPI del sistema 2 responda."""
#        raise NotImplementedError
