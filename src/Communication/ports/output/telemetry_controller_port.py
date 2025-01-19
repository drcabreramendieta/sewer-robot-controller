from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from typing import Callable
"""Telemetry controller port interface definition.

This module defines the abstract interface for telemetry hardware control,
providing methods for callback setup and telemetry listening control.
"""
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