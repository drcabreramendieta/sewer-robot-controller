from abc import ABC, abstractmethod
from Video.domain.entities.video_entities import VideoMessage
"""Abstract interface for video update services.

This module defines the interface for services that manage video stream
updates and observer notifications.

"""
class VideoUpdateServicePort(ABC):
    """Abstract base class for video update services.
    
    Defines interface for managing video updates and observers.
    Implementations must provide methods for updating video frames
    and managing registered observers.
    """
    @abstractmethod
    def update_video(self, msg: VideoMessage) -> None:
        """Update video frame and notify observers.

        Args:
            msg (VideoMessage): New video frame to broadcast

        Raises:
            ValueError: If video frame data is invalid
        """
        pass