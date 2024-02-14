import cv2
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QSlider, QLabel
from PyQt6.QtGui import QImage, QPixmap
from Inspection.ports.robot_controller import RobotController
from Inspection.ports.camera_controller import CameraController
from Video.domain.use_cases.video_notifier import VideoNotifier
from Video.domain.entities import VideoMessage
from Inspection.adapters.qt_video_observer import QtVideoObserver

class MainWindow(QMainWindow):
    video_changed_signal = pyqtSignal(VideoMessage)
    def __init__(self, robot_controller:RobotController, camera_controller:CameraController, video_observer:QtVideoObserver, video_notifier:VideoNotifier) -> None:
        super().__init__()
        self.robot_controller = robot_controller
        self.camera_controller = camera_controller
        self.video_notifier = video_notifier
        self.video_observer = video_observer
        self.video_observer.register_signal(self.video_changed_signal)
        self.video_notifier.register_observer(self.video_observer)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Robot Control')
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        self.btn_forward = QPushButton('Forward')
        self.btn_backward = QPushButton('Backward')
        self.btn_left_forward = QPushButton('Left Forward')
        self.btn_right_forward = QPushButton('Right Forward')
        self.btn_left_backward = QPushButton('Left Backward')
        self.btn_right_backward = QPushButton('Right Backward')

        self.btn_tilt_down = QPushButton('Tilt Down')
        self.btn_tilt_up = QPushButton('Tilt Up')
        self.btn_pan_left = QPushButton('Pan Left')
        self.btn_pan_right = QPushButton('Pan Right')
        self.btn_focus_in = QPushButton('Focus In')
        self.btn_focus_out = QPushButton('Focus Out')
        self.slider_light = QSlider(Qt.Orientation.Horizontal)
        self.slider_light.setMinimum(0)
        self.slider_light.setMaximum(100)
        self.btn_init_camera = QPushButton('Initialize Camera')

        self.disply_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        

        # Connect buttons to command_service methods
        self.btn_forward.pressed.connect(lambda: self.robot_controller.move_forward())
        self.btn_backward.pressed.connect(lambda: self.robot_controller.move_backward())
        self.btn_left_forward.pressed.connect(lambda: self.robot_controller.rotate_left_forward())
        self.btn_right_forward.pressed.connect(lambda: self.robot_controller.rotate_right_forward())
        self.btn_left_backward.pressed.connect(lambda: self.robot_controller.rotate_left_backward())
        self.btn_right_backward.pressed.connect(lambda: self.robot_controller.rotate_right_backward())

        self.btn_forward.released.connect(lambda: self.robot_controller.stop())
        self.btn_backward.released.connect(lambda: self.robot_controller.stop())
        self.btn_left_forward.released.connect(lambda: self.robot_controller.stop())
        self.btn_right_forward.released.connect(lambda: self.robot_controller.stop())
        self.btn_left_backward.released.connect(lambda: self.robot_controller.stop())
        self.btn_right_backward.released.connect(lambda: self.robot_controller.stop())

        self.btn_tilt_down.pressed.connect(lambda: self.camera_controller.tilt_down())
        self.btn_tilt_up.pressed.connect(lambda: self.camera_controller.tilt_up())
        self.btn_pan_left.pressed.connect(lambda: self.camera_controller.pan_left())
        self.btn_pan_right.pressed.connect(lambda: self.camera_controller.pan_right())
        self.btn_focus_in.pressed.connect(lambda: self.camera_controller.focus_in())
        self.btn_focus_out.pressed.connect(lambda: self.camera_controller.focus_out())

        self.btn_init_camera.clicked.connect(lambda: self.camera_controller.init_camera())

        self.btn_tilt_up.released.connect(lambda: self.camera_controller.tilt_stop())
        self.btn_tilt_down.released.connect(lambda: self.camera_controller.tilt_stop())
        self.btn_pan_left.released.connect(lambda: self.camera_controller.pan_stop())
        self.btn_pan_right.released.connect(lambda: self.camera_controller.pan_stop())
        self.btn_focus_in.released.connect(lambda: self.camera_controller.focus_stop())
        self.btn_focus_out.released.connect(lambda: self.camera_controller.focus_stop())
        self.slider_light.valueChanged.connect(lambda value: self.camera_controller.change_light(value))

        self.video_changed_signal.connect(self.update_image)
        self.video_notifier.start_listening()
                                          
        layout.addWidget(self.btn_forward)
        layout.addWidget(self.btn_backward)
        layout.addWidget(self.btn_left_forward)
        layout.addWidget(self.btn_right_forward)
        layout.addWidget(self.btn_left_backward)
        layout.addWidget(self.btn_right_backward)
        
        layout.addWidget(self.btn_tilt_down)
        layout.addWidget(self.btn_tilt_up)
        layout.addWidget(self.btn_pan_left)
        layout.addWidget(self.btn_pan_right)
        layout.addWidget(self.btn_focus_in)
        layout.addWidget(self.btn_focus_out)
        layout.addWidget(self.slider_light)

        layout.addWidget(self.btn_init_camera)
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @pyqtSlot(VideoMessage)
    def update_image(self, video:VideoMessage):
        qt_img = self.convert_cv_qt(video.frame)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)