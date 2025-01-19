from abc import ABC, abstractmethod
from Video.domain.entities.video_entities import VideoMessage
"""Abstract interface for video frame observers.

This module defines the interface for objects that need to receive
notifications about new video frame updates.

"""
class VideoObserverPort(ABC):
    """Abstract base class for video frame observers.
    
    Defines interface for objects that need to be notified
    when new video frames become available.
    """
    @abstractmethod
    def on_video_ready(self, video:VideoMessage) -> None:
        """Handle notification of new video frame.

        Args:
            video (VideoMessage): New video frame data

        Raises:
            ValueError: If video frame data is invalid
        """
        pass