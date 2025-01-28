from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage

class TelemetryObserverPort(ABC):
    """Abstract base class for telemetry data observers.
    
    Defines interface for objects that need to be notified
    when new telemetry data becomes available.
    """

    @abstractmethod
    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        """Handle notification of new telemetry data.

        Args:
            telemetry (TelemetryMessage): New telemetry data update

        Raises:
            ValueError: If telemetry data is invalid
        """
        pass