from abc import ABC, abstractmethod
from Video.domain.entities import ImageInfo, RecordInfo

class DvrLink(ABC):
    @abstractmethod
    def take_image(self) -> ImageInfo:
        pass

    @abstractmethod
    def download_image(self, image_info:ImageInfo) -> str:
        pass

    @abstractmethod
    def download_video(self, record_info:RecordInfo) -> str:
        pass

    @abstractmethod
    def start_recording(self) -> bool:
        pass

    @abstractmethod
    def stop_recording(self) -> RecordInfo:
        pass