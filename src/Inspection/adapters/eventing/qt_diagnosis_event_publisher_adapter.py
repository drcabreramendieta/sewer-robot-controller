from typing import Dict
from PyQt6.QtCore import QObject, pyqtSignal
from Inspection.adapters.eventing.diagnosis_event_notifier import DiagnosisEventNotifier
from Inspection.adapters.eventing.diagnosis_event_publisher import DiagnosisEventPublisher

class _Bridge(QObject):
    event_signal = pyqtSignal(dict)

    def __init__(self, diagnosis_event_notifier: DiagnosisEventNotifier) -> None:
        super().__init__()
        self.event_signal.connect(diagnosis_event_notifier.update_event)

class QtDiagnosisEventPublisherAdapter(DiagnosisEventPublisher):
    """Publica eventos al hilo de Qt mediante señales."""
    def __init__(self, diagnosis_event_notifier: DiagnosisEventNotifier) -> None:
        self._bridge = _Bridge(diagnosis_event_notifier)

    def publish(self, event: Dict[str, any]) -> None:
        self._bridge.event_signal.emit(event)
