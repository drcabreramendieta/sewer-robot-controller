from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class DiagnosisServicesPort(ABC):
    @abstractmethod
    def initialize_system(self) -> Dict[str, Any]:
        """Health-check + precarga (modelos/sesiones). No debe bloquear."""
        pass

    @abstractmethod
    def list_models(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def select_model(self, model_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def list_sessions(self) -> List[str]:
        pass

    @abstractmethod
    def start_diagnosis_session(
        self,
        operator: str,
        location: str,
        job_order: Optional[str] = None,
    ) -> str:
        """Hace TODO: crea session (POST /video/start) + subscribe WS."""
        pass

    @abstractmethod
    def stop_diagnosis_session(self) -> str:
        pass

    @abstractmethod
    def get_summary(
        self,
        session_id: str,
        operator: str,
        location: str,
        job_order: Optional[str] = None,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_current_session_id(self) -> Optional[str]:
        pass
