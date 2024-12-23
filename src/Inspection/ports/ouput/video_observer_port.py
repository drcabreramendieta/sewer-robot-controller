from abc import ABC, abstractmethod
from Video.domain.entities.video_entities import VideoMessage

class VideoObserverPort(ABC):
    @abstractmethod
    def on_video_ready(self, video:VideoMessage) -> None:
        pass