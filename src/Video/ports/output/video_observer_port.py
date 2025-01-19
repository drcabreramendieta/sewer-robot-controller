from abc import ABC, abstractmethod
from Video.domain.entities.video_entities import VideoMessage
"""Abstract interface for video frame observation.

This module defines the interface for objects that need to receive
notifications about new video frames.
"""

class VideoObserverPort(ABC):
    """Abstract base class for video frame observers.

    Defines interface for objects that need to receive video
    frame update notifications.
    """
    @abstractmethod
    def on_video_ready(self, video:VideoMessage) -> None:
        """Handle notification of new video frame.

        Args:
            video (VideoMessage): New video frame data

        Raises:
            RuntimeError: If frame handling fails
        """
        pass