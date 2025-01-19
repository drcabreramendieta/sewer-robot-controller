from abc import ABC, abstractmethod
from typing import Callable
from Video.domain.entities.video_entities import VideoMessage
"""Abstract interface for video stream control.

This module defines the interface for controlling video streams
and managing frame callbacks.
"""
class VideoControllerPort(ABC):
    """Abstract base class for video stream control.

    Defines interface for managing video streams and frame callbacks.
    """
    @abstractmethod
    def callback_setup(self, callback:Callable[[VideoMessage],None]) -> None:
        """Configure callback for video frame updates.

        Args:
            callback (Callable[[VideoMessage], None]): Function to handle new frames

        Raises:
            ValueError: If callback is None
        """
        pass

    @abstractmethod
    def start_listening(self) -> None:
        """Start video frame capture.

        Raises:
            RuntimeError: If start fails
        """
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        """Stop video frame capture.

        Raises:
            RuntimeError: If stop fails
        """
        pass