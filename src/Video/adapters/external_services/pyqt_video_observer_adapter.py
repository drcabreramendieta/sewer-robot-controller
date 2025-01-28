from Video.ports.output import VideoObserverPort
from Video.domain.entities.video_entities import VideoMessage

from Inspection.ports.input import VideoUpdateServicePort
from PyQt6.QtCore import pyqtSignal, QObject
from logging import Logger

class PyqtVideoObserverAdapter(VideoObserverPort):
    """Adapter to integrate video observation with PyQt signals.

    Implements observer pattern using PyQt signals for GUI updates.

    Args:
        video_update_service (VideoUpdateServicePort): Service for processing updates
        logger (Logger): Logger instance for operation tracking

    Attributes:
        video_update_service: Service handling video updates
        logger: Logger for recording operations
        pyqt_signal_connect: Signal handler instance
    """
    def __init__(self, video_update_service:VideoUpdateServicePort, logger:Logger) -> None:
        """Initialize PyQt video observer adapter.

        Args:
            video_update_service (VideoUpdateServicePort): Update handling service
            logger (Logger): Logger for operation tracking

        Raises:
            ValueError: If service or logger is None
        """
        super().__init__()
        self.video_update_service = video_update_service
        self.logger = logger
        self.pyqt_signal_connect = PyqtSignalConnect(self.video_update_service)

    def on_video_ready(self, video:VideoMessage) -> None:
        """Handle notification of new video frame.

        Args:
            video (VideoMessage): New video frame data

        Raises:
            RuntimeError: If signal emission fails
        """
        if self.pyqt_signal_connect.video_updated_signal:
            self.pyqt_signal_connect.video_updated_signal.emit(video)

class PyqtSignalConnect(QObject):
    """PyQt signal handler for video frame updates.

    Provides signal/slot connections for video frame updates.

    Attributes:
        video_updated_signal (pyqtSignal): Signal emitted on frame updates
    """
    video_updated_signal = pyqtSignal(VideoMessage)
    def __init__(self, video_update_service:VideoUpdateServicePort) -> None:
        """Initialize signal connections.

        Args:
            video_update_service (VideoUpdateServicePort): Service to receive updates

        Raises:
            ValueError: If service is None
        """
        super().__init__()
        self.video_update_service = video_update_service
        self.video_updated_signal.connect(self.video_update_service.update_video)