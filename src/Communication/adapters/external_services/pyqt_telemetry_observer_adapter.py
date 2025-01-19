from Communication.ports.output import TelemetryObserverPort
from Communication.domain.entities.telemetry_entities import TelemetryMessage

from Inspection.ports.input import TelemetryUpdateServicePort
from PyQt6.QtCore import pyqtSignal, QObject
from logging import Logger

"""PyQt adapter for telemetry observation and signal handling.

This module provides an implementation of the TelemetryObserverPort interface
using PyQt signals for handling telemetry updates in the GUI application.
"""

class PyqtTelemetryObserverAdapter(TelemetryObserverPort):
    """PyQt adapter for telemetry observation.

    This class implements the TelemetryObserverPort interface and handles
    telemetry updates using PyQt signals.

    Args:
        telemetry_update_service (TelemetryUpdateServicePort): Service for handling telemetry updates
        logger (Logger): Logger instance for error and info logging

    Attributes:
        telemetry_update_service: Service handling telemetry updates
        logger: Logger instance
        pyqt_signal_connect: Signal connection handler
    """
    def __init__(self, telemetry_update_service:TelemetryUpdateServicePort, logger:Logger) -> None:
        """Initialize PyQt telemetry observer adapter.

        Args:
            telemetry_update_service: Service for handling telemetry updates
            logger: Logger instance for error and info logging
        """
        super().__init__()
        self.telemetry_update_service = telemetry_update_service
        self.logger = logger
        self.pyqt_signal_connect = PyqtSignalConnect(self.telemetry_update_service)

    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        """Handle telemetry data readiness by emitting signal.

        Args:
            telemetry (TelemetryMessage): Telemetry message to be processed
        """
        if self.pyqt_signal_connect.telemetry_updated_signal:
            self.pyqt_signal_connect.telemetry_updated_signal.emit(telemetry)

class PyqtSignalConnect(QObject):
    """Handler for PyQt signals in telemetry updates.

    This class manages signal connections between telemetry updates
    and the update service.

    Attributes:
        telemetry_updated_signal (pyqtSignal): Signal emitted when telemetry is updated
        telemetry_update_service: Service handling telemetry updates
    """
    telemetry_updated_signal = pyqtSignal(TelemetryMessage)
    def __init__(self, telemetry_update_service:TelemetryUpdateServicePort) -> None:
        """Initialize signal connections for telemetry updates.

        Args:
            telemetry_update_service: Service for handling telemetry updates
        """
        super().__init__()
        self.telemetry_update_service = telemetry_update_service
        self.telemetry_updated_signal.connect(self.telemetry_update_service.update_telemetry)