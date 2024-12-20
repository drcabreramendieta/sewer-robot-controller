from Video.ports.output.video_controller_port import VideoControllerPort
from typing import Callable
from Video.domain.entities.video_entities import VideoMessage
import cv2
import threading
from logging import Logger

class OpencvVideoControllerAdapter(VideoControllerPort):
    def __init__(self, rtsp_url: str, logger: Logger) -> None:
        super().__init__()
        self.callback = None
        self.rtsp_url = rtsp_url
        self.running = True
        self.cap = None
        self.logger = logger
        self.thread_capture = threading.Thread(target=self.capture_frames)

    def callback_setup(self, callback: Callable[[VideoMessage], None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        self.thread_capture.start()

    def stop_listening(self) -> None:
        self.running = False
        self.thread_capture.join()
        cv2.destroyAllWindows()

    def capture_frames(self):
        self.running = True
        try:
            cap = cv2.VideoCapture(self.rtsp_url)
            if not cap.isOpened():
                self.logger.error("Error opening video stream or file")
                self.running = False
                return

            while self.running:
                ret, frame = cap.read()
                if not ret:
                    self.logger.error("Stream timeout or error in reading frame")
                    break

                self.callback(VideoMessage(frame=frame))
        except cv2.error as e:
            self.logger.error(f"OpenCV error: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            if cap:
                cap.release()
