from abc import ABC, abstractmethod
from Video.domain.entities import VideoMessage

class VideoObserver(ABC):
    @abstractmethod
    def on_video_ready(self, video:VideoMessage) -> None:
        pass