from Inspection.ports.input import TelemetryUpdateServicePort
from Communication.domain.entities.telemetry_entities import TelemetryMessage

from Inspection.ports.ouput import TelemetryObserverPort

class TelemetryUpdateService(TelemetryUpdateServicePort):
    def __init__(self, telemetry_observers:list[TelemetryObserverPort]|None=None) -> None:
        self.telemetry_observers = telemetry_observers if telemetry_observers else [] 
        super().__init__()

    def update_telemetry(self, telemetry: TelemetryMessage) -> None:
        self._notify(telemetry=telemetry)

    def register_observer(self, observer:TelemetryObserverPort):
        self.telemetry_observers.append(observer)

    def _notify(self, telemetry: TelemetryMessage):
        for observer in self.telemetry_observers:
            observer.on_telemetry_ready(telemetry=telemetry)