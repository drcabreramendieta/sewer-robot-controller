from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from typing import Callable

class TelemetryControllerPort(ABC):
    """Abstract interface for telemetry hardware control.

    This interface defines the required methods for implementing
    low-level telemetry control functionality.
    """
    @abstractmethod
    def callback_setup(self, callback: Callable[[TelemetryMessage], None]) -> None:
        """Set up callback function for telemetry message handling.

        Args:
            callback: Function to be called when telemetry messages are received
        """
        pass

    @abstractmethod
    def start_listening(self) -> None:
        """Start listening for telemetry messages from hardware."""
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        """Stop listening for telemetry messages and cleanup resources."""
        pass