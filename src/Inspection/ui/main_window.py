import cv2
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QSize, QRect
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QPushButton, QWidget, QSlider, QLabel, QHBoxLayout
from PyQt6.QtGui import QImage, QPixmap, QIcon
from Inspection.ports.robot_controller import RobotController
from Inspection.ports.camera_controller import CameraController
from Video.domain.use_cases.video_notifier import VideoNotifier
from Video.domain.entities import VideoMessage
from Inspection.adapters.qt_video_observer import QtVideoObserver


class MainWindow(QMainWindow):
    video_changed_signal = pyqtSignal(VideoMessage)

    def __init__(self, robot_controller: RobotController, camera_controller: CameraController, video_observer: QtVideoObserver, video_notifier: VideoNotifier) -> None:
        super().__init__()
        self.robot_controller = robot_controller
        self.camera_controller = camera_controller
        self.video_notifier = video_notifier
        self.video_observer = video_observer
        self.video_observer.register_signal(self.video_changed_signal)
        self.video_notifier.register_observer(self.video_observer)

        self.disply_width = 640
        self.display_height = 480
        self.disply_width_telemetry = 200
        self.display_height_telemetry = 200

        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Layout para video y telemetría a la izquierda
        video_telemetry_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(400, 200)
        video_telemetry_layout.addWidget(self.image_label)

        self.telemetry_label = QLabel('Telemetría')
        video_telemetry_layout.addWidget(self.telemetry_label)

        # Layout para controles a la derecha
        controls_layout = QVBoxLayout()

        # Etiqueta y controles de movimiento
        label_robot_controls = QLabel('Robot Controls')
        label_robot_controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(label_robot_controls)

        movement_layout = QGridLayout()
        self.btn_forward = QPushButton(' Forward')
        self.btn_forward.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Forward.png'))
        self.btn_forward.setIconSize(QSize(45,45))
        self.btn_backward = QPushButton('Backward')
        self.btn_backward.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Backward.png'))
        self.btn_backward.setIconSize(QSize(45,45))
        self.btn_left_forward = QPushButton('Left Forward')
        self.btn_left_forward.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Left Forward.png'))
        self.btn_left_forward.setIconSize(QSize(45,45))
        self.btn_right_forward = QPushButton('Right Forward')
        self.btn_right_forward.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Right Forward.png'))
        self.btn_right_forward.setIconSize(QSize(45,45))
        self.btn_left_backward = QPushButton('Left Backward')
        self.btn_left_backward.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Left Backward.png'))
        self.btn_left_backward.setIconSize(QSize(45,45))
        self.btn_right_backward = QPushButton('Right Backward')
        self.btn_right_backward.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Right Backward.png'))
        self.btn_right_backward.setIconSize(QSize(45,45))

        movement_layout.addWidget(self.btn_left_forward, 0, 0)
        movement_layout.addWidget(self.btn_right_forward, 0, 1)
        movement_layout.addWidget(self.btn_forward, 1, 0, 1, 2)
        movement_layout.addWidget(self.btn_backward, 2, 0, 1, 2)
        movement_layout.addWidget(self.btn_left_backward, 3, 0)
        movement_layout.addWidget(self.btn_right_backward, 3, 1)
        controls_layout.addLayout(movement_layout)

        # Etiqueta y controles de la cámara
        label_camera_controls = QLabel('Camera Controls')
        label_camera_controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(label_camera_controls)

        camera_layout = QGridLayout()
        self.btn_init_camera = QPushButton('Initialize Camera')
        camera_layout.addWidget(self.btn_init_camera, 0, 0, 1, 2)  # Span 2 columns
        self.btn_init_camera.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/init.png'))
        self.btn_init_camera.setIconSize(QSize(45,45))


        self.btn_tilt_down = QPushButton('Tilt Down')
        self.btn_tilt_up = QPushButton('Tilt Up')
        camera_layout.addWidget(self.btn_tilt_down, 1, 0)
        camera_layout.addWidget(self.btn_tilt_up, 1, 1)
        self.btn_tilt_down.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Tilt down.png'))
        self.btn_tilt_down.setIconSize(QSize(45,45))
        self.btn_tilt_up.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Tilt up.png'))
        self.btn_tilt_up.setIconSize(QSize(45,45))

        self.btn_pan_left = QPushButton('Pan Left')
        self.btn_pan_right = QPushButton('Pan Right')
        camera_layout.addWidget(self.btn_pan_left, 2, 0)
        camera_layout.addWidget(self.btn_pan_right, 2, 1)
        self.btn_pan_left.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Pan Left.png'))
        self.btn_pan_left.setIconSize(QSize(45,45))
        self.btn_pan_right.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Pan Right.png'))
        self.btn_pan_right.setIconSize(QSize(45,45))

        self.btn_focus_out = QPushButton('Focus Out')
        self.btn_focus_in = QPushButton('Focus In')
        camera_layout.addWidget(self.btn_focus_out, 3, 0)
        camera_layout.addWidget(self.btn_focus_in, 3, 1)
        controls_layout.addLayout(camera_layout)
        self.btn_focus_out.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Focus Out.png'))
        self.btn_focus_out.setIconSize(QSize(45,45))
        self.btn_focus_in.setIcon(QIcon('/home/iiot/Documents/Terminal/src/Icons/Focus In.png'))
        self.btn_focus_in.setIconSize(QSize(45,45))

        # Slider de luz debajo de los controles de la cámara
        label_light_controls = QLabel('Illumination Controls')
        label_light_controls.setAlignment(Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(label_light_controls)
        self.slider_light = QSlider(Qt.Orientation.Horizontal)
        self.slider_light.setMinimum(0)
        self.slider_light.setMaximum(100)
        controls_layout.addWidget(self.slider_light)

        # Añadir los layouts de video/telemetría y controles al layout principal
        main_layout.addLayout(video_telemetry_layout)
        main_layout.addLayout(controls_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_connections(self):
        # Connect movement buttons
        self.btn_forward.pressed.connect(self.robot_controller.move_forward)
        self.btn_backward.pressed.connect(self.robot_controller.move_backward)
        self.btn_left_forward.pressed.connect(self.robot_controller.rotate_left_forward)
        self.btn_right_forward.pressed.connect(self.robot_controller.rotate_right_forward)
        self.btn_left_backward.pressed.connect(self.robot_controller.rotate_left_backward)
        self.btn_right_backward.pressed.connect(self.robot_controller.rotate_right_backward)

        self.btn_forward.released.connect(self.robot_controller.stop)
        self.btn_backward.released.connect(self.robot_controller.stop)
        self.btn_left_forward.released.connect(self.robot_controller.stop)
        self.btn_right_forward.released.connect(self.robot_controller.stop)
        self.btn_left_backward.released.connect(self.robot_controller.stop)
        self.btn_right_backward.released.connect(self.robot_controller.stop)

        # Connect camera buttons
        self.btn_tilt_down.pressed.connect(self.camera_controller.tilt_down)
        self.btn_tilt_up.pressed.connect(self.camera_controller.tilt_up)
        self.btn_pan_left.pressed.connect(self.camera_controller.pan_left)
        self.btn_pan_right.pressed.connect(self.camera_controller.pan_right)
        self.btn_focus_in.pressed.connect(self.camera_controller.focus_in)
        self.btn_focus_out.pressed.connect(self.camera_controller.focus_out)

        self.btn_tilt_up.released.connect(self.camera_controller.tilt_stop)
        self.btn_tilt_down.released.connect(self.camera_controller.tilt_stop)
        self.btn_pan_left.released.connect(self.camera_controller.pan_stop)
        self.btn_pan_right.released.connect(self.camera_controller.pan_stop)
        self.btn_focus_in.released.connect(self.camera_controller.focus_stop)
        self.btn_focus_out.released.connect(self.camera_controller.focus_stop)

        self.slider_light.valueChanged.connect(self.camera_controller.change_light)
        self.btn_init_camera.clicked.connect(self.camera_controller.init_camera)

        # Connect video update signal
        self.video_changed_signal.connect(self.update_image)
        self.video_notifier.start_listening()

    @pyqtSlot(VideoMessage)
    def update_image(self, video: VideoMessage):
        qt_img = self.convert_cv_qt(video.frame)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
