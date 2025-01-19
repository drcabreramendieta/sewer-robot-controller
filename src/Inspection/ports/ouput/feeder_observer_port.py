from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
"""Abstract interface for feeder update observers.

This module defines the interface for objects that need to receive
notifications about feeder control state changes.

"""
class FeederObserverPort(ABC):
    """Abstract base class for feeder state observers.
    
    Defines interface for objects that need to be notified
    when feeder control state changes occur.
    """
    @abstractmethod
    def on_feeder_ready(self, feeder_control_data:FeederControlData) -> None:
        """Handle notification of feeder state update.

        Args:
            feeder_control_data (FeederControlData): Updated feeder control state

        Raises:
            ValueError: If control data is invalid
        """
        pass