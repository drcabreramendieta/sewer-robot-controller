from abc import ABC, abstractmethod
"""Abstract interface for session control operations.

This module defines the interface for managing inspection session data
including recording, capture and download operations.


"""
class SessionControllerPort(ABC):
    """Abstract base class for session control operations.

    Defines interface for managing inspection sessions including
    recording control, image capture and data management.
    """

    @abstractmethod
    def begin_session(self, name:str) -> bool:
        """Start new inspection session.

        Args:
            name (str): Name for the new session

        Returns:
            bool: True if session started successfully

        Raises:
            ValueError: If name is empty or invalid
        """
        pass
    
    @abstractmethod
    def take_capture(self) -> None:
        """Capture current camera image.

        Raises:
            RuntimeError: If no active session exists
        """
        pass
    
    @abstractmethod
    def start_recording(self) -> None:
        """Start video recording.

        Raises:
            RuntimeError: If recording already in progress
        """
        pass
    
    @abstractmethod
    def stop_recording(self) -> None:
        """Stop current video recording.

        Raises:
            RuntimeError: If no recording in progress
        """
        pass

    @abstractmethod
    def finish_session(self) -> None:
        """End current inspection session.

        Raises:
            RuntimeError: If no active session
        """
        pass

    @abstractmethod
    def is_new(self, name) -> bool:
        """Check if session name is available.

        Args:
            name (str): Session name to check

        Returns:
            bool: True if name is not in use

        Raises:
            ValueError: If name is empty or invalid
        """
        pass
    
    @abstractmethod
    def get_sessions(self) -> list:
        """Get list of available sessions.

        Returns:
            list: Names of existing sessions
        """
        pass
    
    @abstractmethod
    def download_session(self, session_name:str, target_folder:str):
        """Download session data to filesystem.

        Args:
            session_name (str): Name of session to download
            target_folder (str): Destination folder path

        Raises:
            FileNotFoundError: If session does not exist
            PermissionError: If target folder is not writable
        """ 
        pass
