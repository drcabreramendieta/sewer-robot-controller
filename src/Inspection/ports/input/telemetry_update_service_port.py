from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Inspection.ports.ouput import TelemetryObserverPort

class TelemetryUpdateServicePort(ABC):
    @abstractmethod
    def update_telemetry(self, msg: TelemetryMessage) -> None:
        pass

    @abstractmethod
    def register_observer(self, observer:TelemetryObserverPort):
        pass