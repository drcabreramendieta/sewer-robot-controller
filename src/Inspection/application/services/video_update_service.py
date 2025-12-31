from Inspection.ports.input import VideoUpdateServicePort
from Video.domain.entities.video_entities import VideoMessage
from Inspection.ports.ouput import VideoObserverPort
from typing import List

class VideoUpdateService(VideoUpdateServicePort):
    observers:List[VideoObserverPort]
    def __init__(self) -> None:
        super().__init__()
        self.observers = []

    def update_video(self, msg: VideoMessage) -> None:
        self._notify(msg=msg)

    def register_observer(self, observer:VideoObserverPort):
        self.observers.append(observer)

    def _notify(self, msg: VideoMessage):
        for observer in self.observers:
            observer.on_video_ready(video=msg)
