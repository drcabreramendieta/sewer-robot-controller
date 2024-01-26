from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QSlider
from Inspection.ports.robot_controller import RobotController
from Inspection.ports.camera_controller import CameraController

class MainWindow(QMainWindow):
    def __init__(self, robot_controller:RobotController, camera_controller:CameraController) -> None:
        super().__init__()
        self.robot_controller = robot_controller
        self.camera_controller = camera_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Robot Control')
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        self.btn_forward = QPushButton('Forward')
        self.btn_backward = QPushButton('Backward')
        self.btn_left = QPushButton('Left')
        self.btn_right = QPushButton('Right')

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
        

        # Connect buttons to command_service methods
        self.btn_forward.pressed.connect(lambda: self.robot_controller.move_forward())
        self.btn_backward.pressed.connect(lambda: self.robot_controller.move_backward())
        self.btn_left.pressed.connect(lambda: self.robot_controller.rotate_left())
        self.btn_right.pressed.connect(lambda: self.robot_controller.rotate_right())

        self.btn_forward.released.connect(lambda: self.robot_controller.stop())
        self.btn_backward.released.connect(lambda: self.robot_controller.stop())
        self.btn_left.released.connect(lambda: self.robot_controller.stop())
        self.btn_right.released.connect(lambda: self.robot_controller.stop())

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
                                          
        layout.addWidget(self.btn_forward)
        layout.addWidget(self.btn_backward)
        layout.addWidget(self.btn_left)
        layout.addWidget(self.btn_right)
        
        layout.addWidget(self.btn_tilt_down)
        layout.addWidget(self.btn_tilt_up)
        layout.addWidget(self.btn_pan_left)
        layout.addWidget(self.btn_pan_right)
        layout.addWidget(self.btn_focus_in)
        layout.addWidget(self.btn_focus_out)
        layout.addWidget(self.slider_light)

        layout.addWidget(self.btn_init_camera)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)