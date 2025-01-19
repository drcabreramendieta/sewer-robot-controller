from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
from Inspection.ports.ouput import FeederObserverPort
"""Abstract interface for feeder control update services.

This module defines the interface for services that manage feeder control
updates and observer notifications.

"""
class FeederUpdateServicePort(ABC):
    """Abstract base class for feeder update services.

    Defines interface for managing feeder control updates and observers.
    Implementations must provide methods for updating control state,
    sending messages and managing observers.
    """

    @abstractmethod
    def update_feeder_control(self, feeder_control_data:FeederControlData) -> None:
        """Update feeder control state and notify observers.

        Args:
            feeder_control_data (FeederControlData): New feeder control parameters

        Raises:
            ValueError: If control data is invalid
        """
        pass

    @abstractmethod
    def send_message(self, msg:str) -> None:
        """Send control message to feeder hardware.

        Args:
            msg (str): Control message to send

        Raises:
            ConnectionError: If communication with hardware fails
        """
        pass

    @abstractmethod
    def register_observer(self, observer:FeederObserverPort):
        """Register new observer for feeder updates.

        Args:
            observer (FeederObserverPort): Observer instance to receive updates
        """
        pass