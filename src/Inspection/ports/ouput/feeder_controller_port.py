from abc import ABC, abstractmethod

class FeederControllerPort(ABC):
    """Abstract base class for feeder control operations.

    Defines interface for sending control messages to the feeder
    hardware system.
    """

    @abstractmethod
    def send_message(self, msg:str) -> None:
        """Send control message to feeder hardware.

        Args:
            msg (str): Control message to send to feeder

        Raises:
            ConnectionError: If communication with hardware fails
            ValueError: If message format is invalid
        """
        pass