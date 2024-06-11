from Video.ports.video_link import VideoLink
from typing import Callable
from Video.domain.entities import VideoMessage
import cv2
import threading
from logging import Logger

class OpenCVVideoLink(VideoLink):
    def __init__(self, rtsp_url:str, logger:Logger) -> None:
        super().__init__()
        self.callback = None
        self.rtsp_url = rtsp_url
        self.running = True
        self.cap = None
        self.logger = logger
        self.thread_capture = threading.Thread(target=self.capture_frames)

    def callback_setup(self, callback:Callable[[VideoMessage],None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        self.thread_capture.start()
        

    def stop_listening(self) -> None:
        self.running = False
        self.thread_capture.join()
        cv2.destroyAllWindows()


    def capture_frames(self):
        self.running = True
        cap = cv2.VideoCapture(self.rtsp_url)
        if (cap.isOpened()== False): 
            print("Error opening video stream or file")
            self.running = False

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            self.callback(VideoMessage(frame=frame))
        cap.release()