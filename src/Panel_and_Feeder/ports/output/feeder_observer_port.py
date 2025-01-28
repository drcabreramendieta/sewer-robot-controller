from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData

class FeederObserverPort(ABC):
    """Abstract base class for feeder control observers.

    Defines interface for objects that need to receive notifications
    about feeder control state changes.
    """
    @abstractmethod
    def on_feeder_control_data_ready(self, feeder_control_data:FeederControlData) -> None:
        """Handle notification of feeder control update.

        Args:
            feeder_control_data (FeederControlData): Updated feeder state

        Raises:
            ValueError: If control data is invalid
        """
        pass
