from Video.ports.output.video_observer_port import VideoObserverPort
from Video.domain.entities.video_entities import VideoMessage
import cv2

class TestVideoObserver(VideoObserverPort):
    def on_video_ready(self, video:VideoMessage) -> None:
        print(video)