from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage

class TelemetryObserverPort(ABC):
    """Abstract interface for telemetry observers.

    This interface defines the required methods for implementing
    telemetry observation functionality using the Observer pattern.
    """
    @abstractmethod
    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        """Handle new telemetry data availability.

        Args:
            telemetry: New telemetry message to process
        """
        pass