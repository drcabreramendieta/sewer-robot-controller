from typing import Any, Dict, List
from Inspection.ports.input import DiagnosisUpdateServicePort
from Inspection.ports.ouput import DiagnosisObserverPort

class DiagnosisUpdateService(DiagnosisUpdateServicePort):
    def __init__(self) -> None:
        super().__init__()
        self._observers: List[DiagnosisObserverPort] = []

    def register_observer(self, observer: DiagnosisObserverPort) -> None:
        self._observers.append(observer)

    def update_event(self, event: Dict[str, Any]) -> None:
        for obs in self._observers:
            obs.on_diagnosis_event(event)
