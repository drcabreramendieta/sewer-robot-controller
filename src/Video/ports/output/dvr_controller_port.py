from abc import ABC, abstractmethod
from Video.domain.entities.repository_entities import ImageInfo
from Video.domain.entities.repository_entities import RecordInfo
"""Abstract interface for DVR hardware control.

This module defines the interface for controlling DVR hardware
including image capture, video recording and file management.
"""
class DvrControllerPort(ABC):
    """Abstract base class for DVR hardware control.

    Defines interface for controlling DVR operations including
    image capture, video recording and file management.
    """
    @abstractmethod
    def take_image(self) -> ImageInfo:
        """Capture current camera image.

        Returns:
            ImageInfo: Image path and timestamp info

        Raises:
            RuntimeError: If capture fails
        """
        pass

    @abstractmethod
    def download_video(self, json_data, session_name, target_folder):
        """Download recorded video to target folder.

        Args:
            json_data (dict): Video metadata information
            session_name (str): Session identifier
            target_folder (str): Destination folder path
            
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If download fails
        """
        pass

    @abstractmethod
    def search_video(self, json_path, session_name):
        """Search for recorded videos.

        Args:
            json_path (str): Path to search metadata
            session_name (str): Session to search in

        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If search fails
        """
        pass

    @abstractmethod
    def start_recording(self) -> bool:
        """Start video recording.

        Returns:
            bool: True if recording started successfully

        Raises:
            RuntimeError: If start fails
        """
        pass

    @abstractmethod
    def stop_recording(self) -> RecordInfo:
        """Stop current recording.

        Returns:
            RecordInfo: Recording path and timestamp info

        Raises:
            RuntimeError: If stop fails
        """
        pass

    @abstractmethod
    def set_folder(self, name:str) -> None:
        """Set current working folder.

        Args:
            name (str): Folder name to set

        Raises:
            ValueError: If name is invalid
            RuntimeError: If folder creation fails
        """
        pass