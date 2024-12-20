from abc import ABC, abstractmethod
from Video.domain.entities.video_entities import VideoMessage

class VideoUpdateServicePort(ABC):
    @abstractmethod
    def update_video(self, msg: VideoMessage) -> None:
        pass