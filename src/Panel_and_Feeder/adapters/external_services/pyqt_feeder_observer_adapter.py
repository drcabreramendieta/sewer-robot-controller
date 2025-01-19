from Panel_and_Feeder.ports.output import FeederObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData

from Inspection.ports.input import FeederUpdateServicePort
from PyQt6.QtCore import pyqtSignal, QObject
from logging import Logger
"""PyQt adapter for feeder control observation.

This module provides adapters to integrate feeder control operations
with PyQt's signal/slot mechanism.


"""
class PyqtFeederObserverAdapter(FeederObserverPort):
    """Adapter to integrate feeder observation with PyQt signals.

    Implements observer pattern using PyQt signals for GUI updates.

    Args:
        feeder_update_service (FeederUpdateServicePort): Service for processing updates
        logger (Logger): Logger instance for operation tracking

    Attributes:
        feeder_update_service: Service handling feeder updates
        logger: Logger for recording operations
        pyqt_signal_connect: Signal handler instance
    """
    def __init__(self, feeder_update_service:FeederUpdateServicePort, logger:Logger) -> None:
        """Initialize the PyQt feeder observer adapter.

        Args:
            feeder_update_service (FeederUpdateServicePort): Update handling service
            logger (Logger): Logger for operation tracking
        """
        super().__init__()
        self.feeder_update_service = feeder_update_service
        self.logger = logger
        self.pyqt_signal_connect = PyqtSignalConnect(self.feeder_update_service)

    def on_feeder_control_data_ready(self, feeder_control_data:FeederControlData) -> None:
        """Handle new feeder control data updates.

        Args:
            feeder_control_data (FeederControlData): Updated control state

        Raises:
            RuntimeError: If signal emission fails
        """
        if self.pyqt_signal_connect.feeder_control_updated_signal:
            self.pyqt_signal_connect.feeder_control_updated_signal.emit(feeder_control_data)
    

class PyqtSignalConnect(QObject):
    """PyQt signal handler for feeder control updates.

    Manages signal/slot connections for feeder control updates.

    Args:
        feeder_update_service (FeederUpdateServicePort): Service receiving updates

    Attributes:
        feeder_control_updated_signal (pyqtSignal): Signal for feeder updates
        feeder_update_service: Service handling updates
    """
    feeder_control_updated_signal = pyqtSignal(FeederControlData)
    def __init__(self, feeder_update_service:FeederUpdateServicePort) -> None:
        """Initialize signal connections.

        Args:
            feeder_update_service (FeederUpdateServicePort): Update handling service
        """
        super().__init__()
        self.feeder_update_service = feeder_update_service
        self.feeder_control_updated_signal.connect(self.feeder_update_service.update_feeder_control)