from Inspection.ports.input import TelemetryUpdateServicePort
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Inspection.ports.ouput import TelemetryObserverPort
from typing import List

class TelemetryUpdateService(TelemetryUpdateServicePort):
    observers:List[TelemetryObserverPort]
    def __init__(self, observer:TelemetryObserverPort) -> None:
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer) 
        super().__init__()

    def update_telemetry(self, telemetry: TelemetryMessage) -> None:
        self._notify(telemetry=telemetry)

    def register_observer(self, observer:TelemetryObserverPort):
        self.observers.append(observer)

    def _notify(self, telemetry: TelemetryMessage):
        for observer in self.observers:
            observer.on_telemetry_ready(telemetry=telemetry)