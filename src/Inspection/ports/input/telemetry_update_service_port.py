from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage

class TelemetryUpdateServicePort(ABC):
    @abstractmethod
    def update_telemetry(self, msg: TelemetryMessage) -> None:
        pass