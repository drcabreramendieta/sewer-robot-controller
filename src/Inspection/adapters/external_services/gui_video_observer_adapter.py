from Inspection.ports.ouput import VideoObserverPort
from Video.domain.entities.video_entities import VideoMessage
from Inspection.adapters.gui.main_window import MainWindow

import cv2
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
"""GUI adapter for video observation and display.

This module provides an adapter that implements the VideoObserverPort interface
for displaying video frames in the GUI application.
"""

class GuiVideoObserverAdapter(VideoObserverPort):
    """VideoObserverPort adapter for GUI video display.

    This adapter implements the VideoObserverPort interface to display video frames
    in a Qt GUI window. It converts OpenCV image formats to Qt compatible formats
    and updates the GUI's image label with the converted frames.

    Args:
        gui (MainWindow): Main window instance for GUI updates

    Attributes:
        gui: Reference to main window for updating video display
    """
    def __init__(self, gui:MainWindow):
        """Initialize video observer GUI adapter."""
        super().__init__()
        self.gui = gui

    def on_video_ready(self, video:VideoMessage) -> None:
        """Handle new video frame and update GUI display.

        Args:
            video: Video message containing new frame to display
        """
        qt_img = self._convert_cv_qt(video.frame)
        self.gui.image_label.setPixmap(qt_img)

    def _convert_cv_qt(self, cv_img):
        """Convert OpenCV image format to Qt compatible format.

        Args:
            cv_img: Input image in OpenCV format

        Returns:
            QPixmap: Converted image ready for Qt display
        """
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.gui.disply_width, self.gui.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)