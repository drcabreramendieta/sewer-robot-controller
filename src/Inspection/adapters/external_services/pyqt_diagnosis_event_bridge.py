from typing import Any, Dict
from PyQt6.QtCore import QObject, pyqtSignal
from Inspection.ports.input import DiagnosisUpdateServicePort

class _Bridge(QObject):
    event_signal = pyqtSignal(dict)

    def __init__(self, diagnosis_update_service: DiagnosisUpdateServicePort) -> None:
        super().__init__()
        self.event_signal.connect(diagnosis_update_service.update_event)

class PyqtDiagnosisEventBridge:
    """Permite emitir eventos desde hilos (WS thread) hacia el thread de Qt."""
    def __init__(self, diagnosis_update_service: DiagnosisUpdateServicePort) -> None:
        self._bridge = _Bridge(diagnosis_update_service)

    def emit(self, payload: Dict[str, Any]) -> None:
        self._bridge.event_signal.emit(payload)
