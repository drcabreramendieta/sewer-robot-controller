from Inspection.ports.input import SessionServicesPort
from Inspection.ports.ouput import SessionControllerPort

class SessionServices(SessionServicesPort):
    """Service for managing inspection session operations.
    
    Implements session management interface to handle recording, capture
    and data management operations.
    
    Args:
        SessionServicesPort (SessionServicesPort): Base interface defining session operations
    """    
    def __init__(self, session_controller:SessionControllerPort):
        """Initialize session services with controller.
      
        Args:
            session_controller (SessionControllerPort): Controller for session operations
        """        
        super().__init__()
        self.session_controller = session_controller

    def begin_session(self, name:str) -> bool:    
        """Start new inspection session with given name.

        Args:
            name (str): Unique identifier for the session

        Returns:
            bool: True if session started successfully, False otherwise

        Raises:
            ValueError: If name is empty or invalid
        """
        return self.session_controller.begin_session(name=name)
    
    def take_capture(self) -> None:        
        """Capture current camera image and save to session.

        Raises:
            RuntimeError: If no active session exists
        """
        self.session_controller.take_capture()
    
    def start_recording(self) -> None:
        """Start video recording."""
        self.session_controller.start_recording()
    
    def stop_recording(self) -> None:
     
        """Stop current video recording."""
        self.session_controller.stop_recording()

    def finish_session(self) -> None:
        """End current inspection session."""
        self.session_controller.finish_session()

    def is_new(self, name) -> bool:
        """Check if given session name is available for use.

        Validates whether the provided session name has not been used before
        and is available for a new session.

        Args:
            name (str): Session name to validate

        Returns:
            bool: True if name is available, False if already exists

        Raises:
            ValueError: If name is empty or contains invalid characters
        """
        return self.session_controller.is_new(name=name)
    
    def get_sessions(self) -> list:    
        """Get list of available sessions.

        Returns:
            list: Names of available sessions
        """
        return self.session_controller.get_sessions()

    def download_session(self, session_name:str, target_folder:str):
        """Download session data to specified filesystem location.

        Args:
            session_name (str): Name of session to download
            target_folder (str): Destination folder path

        Raises:
            FileNotFoundError: If session does not exist
            PermissionError: If target folder is not writable
        """
        self.session_controller.download_session(session_name=session_name, target_folder=target_folder)
