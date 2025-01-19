from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Inspection.ports.ouput import TelemetryObserverPort
"""Abstract interface for telemetry update services.

This module defines the interface for services that manage telemetry
updates and observer notifications.

"""

class TelemetryUpdateServicePort(ABC):
    """Abstract base class for telemetry update services.

    Defines interface for managing telemetry updates and observers.
    Implementations must provide methods for updating telemetry
    data and managing registered observers.
    """
    @abstractmethod
    def update_telemetry(self, msg: TelemetryMessage) -> None:
        """Update telemetry data and notify observers.

        Args:
            msg (TelemetryMessage): New telemetry data to broadcast

        Raises:
            ValueError: If telemetry data is invalid
        """
        pass

    @abstractmethod
    def register_observer(self, observer:TelemetryObserverPort):
        """Register new observer for telemetry updates.

        Args:
            observer (TelemetryObserverPort): Observer to receive updates

        Raises:
            ValueError: If observer is None or invalid
        """
        pass