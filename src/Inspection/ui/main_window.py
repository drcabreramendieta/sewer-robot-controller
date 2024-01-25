from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget
from Inspection.ports.robot_controller import RobotController

class MainWindow(QMainWindow):
    def __init__(self, robot_controller:RobotController) -> None:
        super().__init__()
        self.robot_controller = robot_controller

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Robot Control')
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        self.btn_forward = QPushButton('Forward')
        self.btn_backward = QPushButton('Backward')
        self.btn_left = QPushButton('Left')
        self.btn_right = QPushButton('Right')

        # Connect buttons to command_service methods
        self.btn_forward.clicked.connect(lambda: self.robot_controller.move_forward())
        self.btn_backward.clicked.connect(lambda: self.robot_controller.move_backward())
        self.btn_left.clicked.connect(lambda: self.robot_controller.rotate_left)
        self.btn_right.clicked.connect(lambda: self.robot_controller.rotate_right())

        layout.addWidget(self.btn_forward)
        layout.addWidget(self.btn_backward)
        layout.addWidget(self.btn_left)
        layout.addWidget(self.btn_right)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)