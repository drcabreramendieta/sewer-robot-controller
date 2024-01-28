from Video.ports.video_observer import VideoObserver
from Video.domain.entities import VideoMessage
import cv2

class TestVideoObserver(VideoObserver):
    def on_video_ready(self, video:VideoMessage) -> None:
        print(video)