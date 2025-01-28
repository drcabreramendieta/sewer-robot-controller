from abc import ABC, abstractmethod
from Panel_and_Feeder.ports.output import PanelObserverPort

class PanelServicesPort(ABC):
    """Abstract base class for panel service operations.

    Defines interface for managing panel control operations and
    observer registrations.
    """
    @abstractmethod
    def register_observer(self, observer:PanelObserverPort):
        """Register new observer for panel updates.

        Args:
            observer (PanelObserverPort): Observer to receive updates

        Raises:
            ValueError: If observer is None
        """
        pass

    @abstractmethod
    def start_listening(self):
        """Start listening for panel control updates.

        Raises:
            RuntimeError: If listening fails to start
        """
        pass

    @abstractmethod
    def stop_listening(self):
        """Stop listening for panel control updates.

        Raises:
            RuntimeError: If listening fails to stop
        """
        pass