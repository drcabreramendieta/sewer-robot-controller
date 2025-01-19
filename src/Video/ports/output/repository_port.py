from Video.domain.entities.repository_entities import ImageInfo
from Video.domain.entities.repository_entities import RecordInfo
from abc import ABC, abstractmethod
"""Abstract interface for session data repository.

This module defines the interface for storing and retrieving
session data including images and recordings.
"""

class RepositoryPort(ABC):
    """Abstract base class for session data repository.

    Defines interface for managing session storage and retrieval.
    """

    @abstractmethod
    def create(self, name:str) -> bool:
        """Create new session.

        Args:
            name (str): Session name

        Returns:
            bool: True if created successfully

        Raises:
            ValueError: If name is invalid
        """

        pass
    
    @abstractmethod
    def add_capture(self, capture:ImageInfo):
        """Add image capture to session.

        Args:
            capture (ImageInfo): Capture information

        Raises:
            RuntimeError: If add fails
        """
        pass

    @abstractmethod
    def add_record(self, record:RecordInfo):
        """Add recording to session.

        Args:
            record (RecordInfo): Recording information

        Raises:
            RuntimeError: If add fails
        """

        pass
    
    @abstractmethod
    def update_status(self, recording:bool):
        """Update session recording status.

        Args:
            recording (bool): Recording state
            

        Raises:
            RuntimeError: If update fails
        """
        pass
    
    @abstractmethod
    def get_status(self):
        """Get current recording status.

        Raises:
            RuntimeError: If query fails 
        """
        pass
    
    @abstractmethod
    def session_exists(self, name):
        """Check if session exists.

        Args:
            name (str): Session name to check

        Raises:
            ValueError: If name invalid
        """
        pass

    @abstractmethod
    def print_session(self):
        """Print current session data.

        Raises:
            RuntimeError: If print fails
        """
        pass
    
    @abstractmethod
    def print_all_sessions(self):
        """Print all session data.

        Raises:
            RuntimeError: If print fails
        """
        pass
    
    @abstractmethod
    def get_session(self, name:str)->dict:
        """Get session by name.

        Args:
            name (str): Session name

        Returns:
            dict: Session data

        Raises:
            ValueError: If name invalid
        """
        pass

    @abstractmethod
    def get_sessions(self):
        """Get all sessions.

        Returns:
            list: List of sessions

        Raises:
            RuntimeError: If query fails
        """
        pass

    @abstractmethod
    def is_session_attached(self):
        """Check if session is attached."""
        pass