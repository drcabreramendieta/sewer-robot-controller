from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage

class TelemetryObserverPort(ABC):
    @abstractmethod
    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        pass