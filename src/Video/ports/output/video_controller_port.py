from abc import ABC, abstractmethod
from typing import Callable
from Video.domain.entities.video_entities import VideoMessage

class VideoControllerPort(ABC):
    @abstractmethod
    def callback_setup(self, callback:Callable[[VideoMessage],None]) -> None:
        pass

    @abstractmethod
    def start_listening(self) -> None:
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        pass