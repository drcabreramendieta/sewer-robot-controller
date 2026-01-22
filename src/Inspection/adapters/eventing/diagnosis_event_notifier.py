from typing import Any, Dict, List
from Inspection.ports.output import DiagnosisObserverPort

class DiagnosisEventNotifier:
    def __init__(self) -> None:
        self._observers: List[DiagnosisObserverPort] = []

    def register_observer(self, observer: DiagnosisObserverPort) -> None:
        self._observers.append(observer)

    def update_event(self, event: Dict[str, Any]) -> None:
        for obs in self._observers:
            obs.on_diagnosis_event(event)
