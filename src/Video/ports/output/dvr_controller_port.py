from abc import ABC, abstractmethod
from Video.domain.entities.repository_entities import ImageInfo
from Video.domain.entities.repository_entities import RecordInfo

class DvrControllerPort(ABC):
    @abstractmethod
    def take_image(self) -> ImageInfo:
        pass

    @abstractmethod
    def download_video(self, session_info, target_folder):
        pass

    @abstractmethod
    def search_video(self, session_info):
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