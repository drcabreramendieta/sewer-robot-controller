from Inspection.ports.input import VideoUpdateServicePort
from Video.domain.entities.video_entities import VideoMessage
from ui.main_window import MainWindow

import cv2
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt

class VideoUpdateService(VideoUpdateServicePort):
    def __init__(self, gui:MainWindow):
        super().__init__()
        self.gui = gui

    def update_video(self, msg: VideoMessage) -> None:
        qt_img = self._convert_cv_qt(msg.frame)
        self.gui.image_label.setPixmap(qt_img)

    def _convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.gui.disply_width, self.gui.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)