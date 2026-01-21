from abc import ABC, abstractmethod
from typing import Any, Dict
from Inspection.ports.ouput import DiagnosisObserverPort

class DiagnosisUpdateServicePort(ABC):
    @abstractmethod
    def update_event(self, event: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def register_observer(self, observer: DiagnosisObserverPort) -> None:
        pass
