from Inspection.ports.input import VideoUpdateServicePort
from Video.domain.entities.video_entities import VideoMessage
from Inspection.ports.ouput import VideoObserverPort

class VideoUpdateService(VideoUpdateServicePort):
    def __init__(self, observers:list[VideoObserverPort]|None=None) -> None:
        self.observers = observers if observers else [] 
        super().__init__()

    def update_video(self, msg: VideoMessage) -> None:
        self._notify(msg=msg)

    def register_observer(self, observer:VideoObserverPort):
        self.observers.append(observer)

    def _notify(self, msg: VideoMessage):
        for observer in self.observers:
            observer.on_video_ready(video=msg)