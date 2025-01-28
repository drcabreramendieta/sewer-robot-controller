from Video.ports.output.video_controller_port import VideoControllerPort
from typing import Callable
from Video.domain.entities.video_entities import VideoMessage
import cv2
import threading
from logging import Logger

class OpencvVideoControllerAdapter(VideoControllerPort):
    """Adapter for controlling video streams with OpenCV.

    Args:
        rtsp_url (str): RTSP stream URL to capture
        logger (Logger): Logger for operation tracking

    Attributes:
        callback: Function to receive frame updates
        rtsp_url: Source stream URL
        running: Thread control flag
        cap: VideoCapture instance
        logger: Operations logger
        thread_capture: Background capture thread
    """
    def __init__(self, rtsp_url: str, logger: Logger) -> None:
        """Initialize OpenCV video controller.

        Args:
            rtsp_url (str): RTSP stream URL
            logger (Logger): Logger instance

        Raises:
            ValueError: If URL or logger is invalid
        """
        super().__init__()
        self.callback = None
        self.rtsp_url = rtsp_url
        self.running = True
        self.cap = None
        self.logger = logger
        self.thread_capture = threading.Thread(target=self.capture_frames)

    def callback_setup(self, callback: Callable[[VideoMessage], None]) -> None:
        """Configure callback for frame updates.

        Args:
            callback (Callable[[VideoMessage], None]): Function to handle new frames

        Raises:
            ValueError: If callback is None
        """
        self.callback = callback

    def start_listening(self) -> None:
        """Start video frame capture thread.

        Raises:
            RuntimeError: If thread fails to start
        """
        self.thread_capture.start()

    def stop_listening(self) -> None:
        """Stop video capture and cleanup resources.

        Raises:
            RuntimeError: If thread fails to stop
        """
        self.running = False
        self.thread_capture.join()
        cv2.destroyAllWindows()

    def capture_frames(self):
        """Capture video frames in background thread.

        Continuously captures frames from RTSP stream and sends
        them to callback function.

        Raises:
            cv2.error: If OpenCV operations fail
            RuntimeError: If stream connection fails
        """
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
