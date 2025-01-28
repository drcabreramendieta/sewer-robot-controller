from Video.ports.input import SessionServicesPort
from Video.ports.output.dvr_controller_port import DvrControllerPort
from Video.ports.output.repository_port import RepositoryPort
from Video.domain.entities.dvr_entities import DvrOrder
import shutil
import os
from logging import Logger

class SessionServices(SessionServicesPort):
    """Service for managing inspection sessions and recordings.

    Args:
        dvr_controller (DvrControllerPort): DVR hardware controller
        repository (RepositoryPort): Session data repository
        logger (Logger): Logger for operation tracking

    Attributes:
        dvr_controller: Hardware control interface
        repository: Data storage interface
        logger: Operations logger
    """
    def __init__(self, dvr_controller: DvrControllerPort, repository: RepositoryPort, logger: Logger) -> None:
        """Initialize session services.

        Args:
            dvr_controller (DvrControllerPort): DVR hardware interface
            repository (RepositoryPort): Data storage interface
            logger (Logger): Logger instance

        Raises:
            ValueError: If required dependencies are invalid
        """
        self.dvr_controller = dvr_controller
        self.repository = repository
        self.logger = logger

    def create_session(self, name: str) -> bool:
        """Create new inspection session.

        Args:
            name (str): Name for the new session

        Returns:
            bool: True if session created successfully

        Raises:
            Exception: If creation fails
        """
        try:
            if self.repository.create(name=name):
                self.dvr_controller.set_folder(name=name)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error creating session '{name}': {e}")
            return False

    def name_exists(self, name: str) -> bool:
        """Check if session name exists.

        Args:
            name (str): Session name to check

        Returns:
            bool: True if name exists

        Raises:
            Exception: If check fails
        """
        try:
            return self.repository.session_exists(name=name)
        except Exception as e:
            self.logger.error(f"Error checking if session name exists '{name}': {e}")
            return False

    def get_sessions(self) -> list:
        """Get list of available sessions.

        Returns:
            list: List of session names

        Raises:
            Exception: If query fails
        """
        try:
            sessions = self.repository.get_sessions()
            return [session["name"] for session in sessions]
        except Exception as e:
            self.logger.error(f"Error getting sessions: {e}")
            return []

    def download_session(self, session_name, target_folder):
        """Download session data to target folder.

        Args:
            session_name (str): Name of session to download
            target_folder (str): Destination folder path

        Returns:
            bool: True if download successful, False if failed, None if no content

        Raises:
            Exception: If download fails
        """
        try:
            os.makedirs(target_folder, exist_ok=True)
            session_info = self.repository.get_session(session_name)
            self.logger.info(f"Session info: {session_info}")

            if not session_info:
                self.logger.error(f"Session '{session_name}' not found.")
                return False

            self.logger.info(f"Session '{session_name}' found.")
            content_found = False

            captures = session_info.get("captures", [])
            if captures:
                content_found = True
                
                for capture in captures:
                    try:
                        source_path = capture["path"]
                        if os.path.exists(source_path):
                            file_name = os.path.basename(source_path)
                            destination_path = os.path.join(target_folder, file_name)
                            shutil.copy(source_path, destination_path)
                            self.logger.info(f"File '{file_name}' copied successfully.")
                            image_success = True
                        else:
                            self.logger.error(f"File '{source_path}' does not exist and cannot be copied.")
                            image_success = False
                    except Exception as e:
                        self.logger.error(f"Error processing image '{source_path}': {e}")
                        image_success = False

            [video_uris, search_success] = self.dvr_controller.search_video(session_info)
            if search_success == False:
                video_success = False
            else:
                video_success = True
            if video_uris:
                content_found = True
                video_success = self.dvr_controller.download_video(session_info, target_folder)
                video_success = True
            if not content_found:
                self.logger.info(f"No videos or images found for session '{session_name}'.")
                video_success = False
                return None

            if image_success and video_success:
                self.logger.info(f"All images and videos processed successfully for session '{session_name}'.")
                return True
            else:
                if not image_success:
                    self.logger.error(f"Some images could not be processed for session '{session_name}'.")
                if not video_success:
                    self.logger.error(f"Videos could not be processed for session '{session_name}'.")
                return False

        except Exception as e:
            self.logger.error(f"Error downloading session '{session_name}': {e}")
            return False

    def run(self, order: DvrOrder):
        """Execute DVR control order.

        Args:
            order (DvrOrder): Control order to execute

        Raises:
            Exception: If order execution fails
        """
        try:
            if self.repository.is_session_attached():
                if order == DvrOrder.TAKE_PHOTO:
                    self.repository.add_capture(self.dvr_controller.take_image())
                elif order == DvrOrder.START_RECORDING:
                    self.repository.update_status(self.dvr_controller.start_recording())
                elif order == DvrOrder.STOP_RECORDING and self.repository.get_status():
                    self.repository.add_record(self.dvr_controller.stop_recording())
                    self.repository.update_status(recording=False)
        except Exception as e:
            self.logger.error(f"Error running order '{order}': {e}")
