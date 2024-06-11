from Video.ports.video_observer import VideoObserver
from Video.domain.entities import VideoMessage
from PyQt6.QtCore import pyqtSignal
from logging import Logger

class QtVideoObserver(VideoObserver):
    video_changed_signal = pyqtSignal(VideoMessage)
    def __init__(self, logger:Logger) -> None:
        super().__init__()
        self.video_changed_signal = None
        self.logger = logger
        
    def on_video_ready(self, video:VideoMessage) -> None:
        if self.video_changed_signal:
            self.video_changed_signal.emit(video)

    def register_signal(self, signal:pyqtSignal):
        self.video_changed_signal = signal