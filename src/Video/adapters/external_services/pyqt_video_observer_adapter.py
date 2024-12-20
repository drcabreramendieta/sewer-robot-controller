from Video.ports.output import VideoObserverPort
from Video.domain.entities.video_entities import VideoMessage

from Inspection.ports.input import VideoUpdateServicePort
from PyQt6.QtCore import pyqtSignal, QObject
from logging import Logger

class PyqtVideoObserverAdapter(VideoObserverPort):
    def __init__(self, video_update_service:VideoUpdateServicePort, logger:Logger) -> None:
        super().__init__()
        self.video_update_service = video_update_service
        self.logger = logger
        self.pyqt_signal_connect = PyqtSignalConnect(self.video_update_service)

    def on_video_ready(self, video:VideoMessage) -> None:
        if self.pyqt_signal_connect.video_updated_signal:
            self.pyqt_signal_connect.video_updated_signal.emit(video)

class PyqtSignalConnect(QObject):
    video_updated_signal = pyqtSignal(VideoMessage)
    def __init__(self, video_update_service:VideoUpdateServicePort) -> None:
        super().__init__()
        self.video_update_service = video_update_service
        self.video_updated_signal.connect(self.video_update_service.update_video)