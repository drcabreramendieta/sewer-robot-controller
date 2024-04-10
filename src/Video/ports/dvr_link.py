from abc import ABC, abstractmethod
from Video.domain.entities import ImageInfo, RecordInfo

class DvrLink(ABC):
    @abstractmethod
    def take_image(self) -> ImageInfo:
        pass

    @abstractmethod
    def download_video(self, json_data, session_name, target_folder):
        pass

    @abstractmethod
    def search_video(self, json_path, session_name):
        pass

    @abstractmethod
    def start_recording(self) -> bool:
        pass

    @abstractmethod
    def stop_recording(self) -> RecordInfo:
        pass

    @abstractmethod
    def set_folder(self, name:str) -> None:
        pass