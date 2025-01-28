from abc import ABC, abstractmethod
from Video.domain.entities.dvr_entities import DvrOrder

class SessionServicesPort(ABC):
    """Abstract base class for session management services.

    Defines interface for managing inspection sessions and recordings.
    """
    @abstractmethod
    def create_session(self, name: str) -> bool:
        """Create new inspection session.

        Args:
            name (str): Name for the new session

        Returns:
            bool: True if session created successfully

        Raises:
            ValueError: If name is invalid
        """
        pass

    @abstractmethod
    def name_exists(self, name: str) -> bool:
        """Check if session name exists.

        Args:
            name (str): Session name to check

        Returns:
            bool: True if name exists

        Raises:
            ValueError: If name is invalid
        """
        pass

    @abstractmethod
    def get_sessions(self) -> list:
        """Get list of available sessions.

        Returns:
            list: List of session names

        Raises:
            RuntimeError: If query fails
        """
        pass

    @abstractmethod
    def download_session(self, session_name, target_folder):
        """Download session data to target folder.

        Args:
            session_name (str): Name of session to download
            target_folder (str): Destination folder path

        Returns:
            bool: True if download successful

        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If download fails
        """
        pass

    @abstractmethod
    def run(self, order: DvrOrder):
        """Execute DVR control order.

        Args:
            order (DvrOrder): Control order to execute

        Raises:
            ValueError: If order is invalid
            RuntimeError: If execution fails
        """
        pass
