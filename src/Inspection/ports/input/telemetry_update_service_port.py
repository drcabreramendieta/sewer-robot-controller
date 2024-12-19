from abc import ABC, abstractmethod

class TelemetryUpdateServicePort(ABC):
    @abstractmethod
    def update_telemetry(self) -> None:
        pass