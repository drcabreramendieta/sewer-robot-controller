from abc import ABC, abstractmethod
from Communication.domain.entities import Telemetry

class TelemetryObserver(ABC):
    @abstractmethod
    def on_telemetry_ready(self, telemetry:Telemetry) -> None:
        pass