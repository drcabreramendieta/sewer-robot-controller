from Inspection.ports.input import VideoUpdateServicePort
from Video.domain.entities.video_entities import VideoMessage
from Inspection.ports.ouput import VideoObserverPort
from typing import List
"""Video update service implementing observer pattern.

This module provides services for managing video stream updates and
notifying registered observers of new video frames.

Typical usage:
    video_service = VideoUpdateService(observer)
    video_service.update_video(frame)
"""

class VideoUpdateService(VideoUpdateServicePort):
    """Service for managing video updates and notifications.

    Implements observer pattern to broadcast video updates to registered observers.

    Args:
        VideoUpdateServicePort: Base interface for video update services

    Attributes:
        observers (List[VideoObserverPort]): List of registered observers
        observer (VideoObserverPort): Primary observer instance
    """
    observers:List[VideoObserverPort]
    def __init__(self, observer:VideoObserverPort) -> None:
        """Initialize video update service.

        Args:
            observer (VideoObserverPort): Initial observer for video updates
        """
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer) 
        super().__init__()

    def update_video(self, msg: VideoMessage) -> None:
        """Update video frame and notify observers.

        Args:
            msg (VideoMessage): New video frame to broadcast

        Raises:
            ValueError: If video frame data is invalid
        """
        self._notify(msg=msg)

    def register_observer(self, observer:VideoObserverPort):
        """Register new observer for video updates.

        Args:
            observer (VideoObserverPort): Observer instance to receive updates
        """
        self.observers.append(observer)

    def _notify(self, msg: VideoMessage):
        """Notify all registered observers of new video frame.

        Args:
            msg (VideoMessage): Video frame to broadcast to observers
        """
        for observer in self.observers:
            observer.on_video_ready(video=msg)