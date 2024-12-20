from Video.ports.input import SessionServicesPort
from Video.ports.output.dvr_controller_port import DvrControllerPort
from Video.ports.output.repository_port import RepositoryPort
from Video.domain.entities.dvr_entities import DvrOrder
import shutil
import os
from logging import Logger

class SessionServices(SessionServicesPort):
    def __init__(self, dvr_link: DvrControllerPort, db_link: RepositoryPort, logger: Logger) -> None:
        self.dvr_link = dvr_link
        self.db_link = db_link
        self.logger = logger

    def create_session(self, name: str) -> bool:
        try:
            if self.db_link.create(name=name):
                self.dvr_link.set_folder(name=name)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error creating session '{name}': {e}")
            return False

    def name_exists(self, name: str) -> bool:
        try:
            return self.db_link.session_exists(name=name)
        except Exception as e:
            self.logger.error(f"Error checking if session name exists '{name}': {e}")
            return False

    def get_sessions(self) -> list:
        try:
            sessions = self.db_link.get_sessions()
            return [session["name"] for session in sessions]
        except Exception as e:
            self.logger.error(f"Error getting sessions: {e}")
            return []

    def download_session(self, session_name, target_folder):
        try:
            os.makedirs(target_folder, exist_ok=True)
            session_info = self.db_link.get_session(session_name)
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

            [video_uris, search_success] = self.dvr_link.search_video(session_info)
            if search_success == False:
                video_success = False
            else:
                video_success = True
            if video_uris:
                content_found = True
                video_success = self.dvr_link.download_video(session_info, target_folder)
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
        try:
            if self.db_link.is_session_attached():
                if order == DvrOrder.TAKE_PHOTO:
                    self.db_link.add_capture(self.dvr_link.take_image())
                elif order == DvrOrder.START_RECORDING:
                    self.db_link.update_status(self.dvr_link.start_recording())
                elif order == DvrOrder.STOP_RECORDING and self.db_link.get_status():
                    self.db_link.add_record(self.dvr_link.stop_recording())
                    self.db_link.update_status(recording=False)
        except Exception as e:
            self.logger.error(f"Error running order '{order}': {e}")
