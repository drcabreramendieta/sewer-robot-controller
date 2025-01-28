from Inspection.ports.ouput.session_controller_port import SessionControllerPort
from Video.application.services.session_services import SessionServices
from Video.domain.entities.dvr_entities import DvrOrder
from logging import Logger

class VideoSessionControllerAdapter(SessionControllerPort):

     
    """Adapter for controlling video recording sessions.

    This adapter implements the SessionControllerPort interface to manage
    video recording sessions, captures and downloads.

    Args:
        control_session: Service for managing recording sessions
        logger: Logger instance for error and info logging

    Attributes:
        control_session: Interface to session control services
        logger: Logger instance
    """
    def __init__(self, control_session:SessionServices, logger:Logger) -> None:
        """Initialize video session controller adapter."""
        super().__init__()
        self.control_session = control_session
        self.logger = logger

    def begin_session(self, name:str) -> bool:
        """Start a new recording session.

        Args:
            name: Name for the new session

        Returns:
            bool: True if session was created successfully
        """
        return self.control_session.create_session(name)
    
    def take_capture(self) -> None:
        """Take a photo capture in current session."""
        print('take capture')
        self.control_session.run(DvrOrder.TAKE_PHOTO)
    
    def start_recording(self) -> None:
        """Start video recording in current session."""
        print('start recording')
        self.control_session.run(DvrOrder.START_RECORDING)
    
    def stop_recording(self) -> None:
        """Stop current video recording."""
        print('stop recording')
        self.control_session.run(DvrOrder.STOP_RECORDING)

    def finish_session(self) -> None:
        """End current recording session."""
        print('No implementado')

    def is_new(self, name) -> bool:
        """Check if session name is available.

        Args:
            name: Session name to check

        Returns:
            bool: True if name is not already used
        """
        return not self.control_session.name_exists(name)
    
    def get_sessions(self) -> list:
        """Get list of available recording sessions.

        Returns:
            list: List of session names
        """
        return self.control_session.get_sessions()
    
    def download_session(self, session_name, target_folder):
        """Download session recordings to target folder.

        Args:
            session_name: Name of session to download
            target_folder: Destination folder path

        Returns:
            bool: True if download was successful
        """ 
        return self.control_session.download_session(session_name, target_folder)