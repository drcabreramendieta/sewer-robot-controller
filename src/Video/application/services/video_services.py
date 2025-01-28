from Video.ports.input import VideoServicesPort
from Video.ports.output.video_observer_port import VideoObserverPort
from Video.domain.entities.video_entities import VideoMessage
from Video.ports.output.video_controller_port import VideoControllerPort
from logging import Logger
from typing import List

class VideoServices(VideoServicesPort):
    """Service for managing video stream processing.

    Implements video processing services including observer pattern
    for frame updates.

    Args:
        video_controller (VideoControllerPort): Video hardware controller
        logger (Logger): Logger for operation tracking
        observer (VideoObserverPort): Initial observer for updates

    Attributes:
        observers (List[VideoObserverPort]): List of registered observers
        video_controller: Hardware control interface
        logger: Operations logger
    """
    observers:List[VideoObserverPort]
    def __init__(self, video_controller:VideoControllerPort, logger:Logger, observer:VideoObserverPort) -> None:
        """Initialize video services.

        Args:
            video_controller (VideoControllerPort): Video controller interface
            logger (Logger): Logger for operation tracking
            observer (VideoObserverPort): Initial update observer

        Raises:
            ValueError: If controller or logger is None
        """
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer)
        self.video_controller = video_controller
        self.logger = logger
        video_controller.callback_setup(self._notify)
        super().__init__()

    def _notify(self, video:VideoMessage) -> None:
        """Notify all observers of video frame update.

        Args:
            video (VideoMessage): New video frame data

        Raises:
            RuntimeError: If notification fails
        """
        for observer in self.observers:
            observer.on_video_ready(video=video)

    def register_observer(self, observer:VideoObserverPort):
        """Register new observer for video updates.

        Args:
            observer (VideoObserverPort): Observer to receive updates

        Raises:
            ValueError: If observer is None
        """
        self.observers.append(observer)

    def start_listening(self):
        """Start listening for video frame updates.

        Raises:
            RuntimeError: If listening fails to start
        """
        print('start')
        self.video_controller.start_listening()

    def stop_listening(self):
        """Stop listening for video frame updates.

        Raises:
            RuntimeError: If listening fails to stop
        """
        self.video_controller.stop_listening()