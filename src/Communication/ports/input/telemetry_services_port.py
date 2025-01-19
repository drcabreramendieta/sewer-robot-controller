from abc import ABC, abstractmethod
from Communication.ports.output import TelemetryObserverPort

class TelemetryServicesPort(ABC):
    """Abstract interface for telemetry control services.

    This interface defines the required methods for implementing
    telemetry data collection and observer management functionality.
    """
    @abstractmethod
    def register_observer(self, observer:TelemetryObserverPort):
        """Register a new telemetry observer.

        Args:
            observer: New observer to register for telemetry updates
        """
        pass

    @abstractmethod
    def start_listening(self) -> None:
        """Start listening for telemetry data updates."""
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        """Stop listening for telemetry data updates."""
        pass