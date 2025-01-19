from Communication.ports.input import TelemetryServicesPort
from Communication.ports.output import TelemetryObserverPort
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Communication.ports.output import TelemetryControllerPort
from logging import Logger
from typing import List
"""Telemetry services implementation.

This module provides services for managing telemetry data collection,
observer registration, and real-time telemetry updates handling.
"""

class TelemetryServices(TelemetryServicesPort):
    """Service class for managing telemetry operations.

    This class implements the TelemetryServicesPort interface and provides
    methods to handle telemetry data collection and observer notifications.

    Args:
        telemetry_controller: Controller for telemetry operations
        logger: Logger instance for error and info logging
        telemetry_observer: Initial observer for telemetry updates

    Attributes:
        observers: List of registered telemetry observers
        telemetry_controller: Interface to control telemetry hardware
        logger: Logger instance
    """
    observers:List[TelemetryObserverPort]
    def __init__(self, telemetry_controller:TelemetryControllerPort, logger:Logger, telemetry_observer:TelemetryObserverPort) -> None:
        """Initialize telemetry services with controller and observer."""
        self.observer = telemetry_observer
        if self.observer:
            self.observers.append(self.observer) 
        self.telemetry_controller = telemetry_controller
        self.logger = logger
        telemetry_controller.callback_setup(self._notify)
        
        super().__init__()

    def _notify(self, telemetry:TelemetryMessage) -> None:
        """Notify all registered observers of new telemetry data.

        Args:
            telemetry: New telemetry message to distribute
        """
        for observer in self.observers:
            observer.on_telemetry_ready(telemetry=telemetry)

    def register_observer(self, observer:TelemetryObserverPort):
        """Register a new telemetry observer.

        Args:
            observer: New observer to register
        """
        self.observers.append(observer)

    def start_listening(self):
        """Start listening for telemetry updates."""
        self.telemetry_controller.start_listening()

    def stop_listening(self):
        """Stop listening for telemetry updates."""
        self.telemetry_controller.stop_listening()