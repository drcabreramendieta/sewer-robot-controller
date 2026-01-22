from abc import ABC, abstractmethod
from typing import Any, Dict


class DiagnosisEventPublisher(ABC):
    @abstractmethod
    def publish(self, event: Dict[str, Any]) -> None:
        pass
