from abc import ABC, abstractmethod
from Video.ports.output.video_observer_port import VideoObserverPort

class VideoServicesPort(ABC):
    """Abstract base class for video stream services.

    Defines interface for managing video stream processing and
    observer registrations.
    """
    @abstractmethod
    def register_observer(self, observer:VideoObserverPort):
        """Register new observer for video updates.

        Args:
            observer (VideoObserverPort): Observer to receive updates

        Raises:
            ValueError: If observer is None
        """
        pass

    @abstractmethod
    def start_listening(self):
        """Start listening for video frame updates.

        Raises:
            RuntimeError: If listening fails to start
        """
        pass

    @abstractmethod
    def stop_listening(self):
        """Stop listening for video frame updates.

        Raises:
            RuntimeError: If listening fails to stop
        """
        pass