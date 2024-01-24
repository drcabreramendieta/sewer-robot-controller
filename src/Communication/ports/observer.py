from abc import ABC, abstractmethod
from Communication.domain.entities import TelemetryMessage

class TelemetryObserver(ABC):
    @abstractmethod
    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        pass