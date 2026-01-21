from abc import ABC, abstractmethod
from typing import Any, Dict

class DiagnosisObserverPort(ABC):
    @abstractmethod
    def on_diagnosis_event(self, event: Dict[str, Any]) -> None:
        pass


#    @abstractmethod
#    def on_diagnosis_status(self, message: str) -> None:
#        raise NotImplementedError