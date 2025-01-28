from abc import ABC, abstractmethod
from Panel_and_Feeder.ports.output import FeederObserverPort

class FeederServicesPort(ABC):
    """Abstract base class for feeder service operations.

    Defines interface for managing feeder control operations and
    observer registrations.
    """
    @abstractmethod
    def register_observer(self, observer:FeederObserverPort):
        """Register new observer for feeder updates.

        Args:
            observer (FeederObserverPort): Observer to receive updates

        Raises:
            ValueError: If observer is None
        """
        pass

    @abstractmethod
    def start_listening(self):
        """Start listening for feeder control updates.

        Raises:
            RuntimeError: If listening fails to start
        """
        pass

    @abstractmethod
    def stop_listening(self):
        """Stop listening for feeder control updates.

        Raises:
            RuntimeError: If listening fails to stop
        """
        pass

    @abstractmethod
    def send_message(self, message:str):
        """Send control message to feeder hardware.

        Args:
            message (str): Control message to send

        Raises:
            RuntimeError: If message sending fails
            ValueError: If message is empty
        """
        pass