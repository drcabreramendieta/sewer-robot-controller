from Inspection.ports.input import TelemetryUpdateServicePort
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Inspection.ports.ouput import TelemetryObserverPort
from typing import List

class TelemetryUpdateService(TelemetryUpdateServicePort):
    """Service for managing telemetry updates and notifications.

    Implements observer pattern to broadcast telemetry updates to 
    registered observers.

    Args:
        TelemetryUpdateServicePort: Base interface for telemetry services

    Attributes:
        observers (List[TelemetryObserverPort]): List of registered observers
        observer (TelemetryObserverPort): Primary observer instance
    """ 
    observers:List[TelemetryObserverPort]
    def __init__(self, observer:TelemetryObserverPort) -> None:
        """Initialize telemetry update service.

        Args:
            observer (TelemetryObserverPort): Initial observer for telemetry updates
        """
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer) 
        super().__init__()

    def update_telemetry(self, telemetry: TelemetryMessage) -> None:
        """Update telemetry data and notify observers.

        Args:
            telemetry (TelemetryMessage): New telemetry data to broadcast

        Raises:
            ValueError: If telemetry data is invalid
        """
        self._notify(telemetry=telemetry)

    def register_observer(self, observer:TelemetryObserverPort):
        """Register new observer for telemetry updates.

        Args:
            observer (TelemetryObserverPort): Observer instance to receive updates
        """
        self.observers.append(observer)

    def _notify(self, telemetry: TelemetryMessage):
        """Notify all registered observers of telemetry update.

        Args:
            telemetry (TelemetryMessage): Telemetry data to broadcast
        """
      
        for observer in self.observers:
            observer.on_telemetry_ready(telemetry=telemetry)