from Panel_and_Feeder.ports.panel_observer import PanelObserver
from Panel_and_Feeder.domain.entities import RobotControlData, CameraControlData
from PyQt6.QtCore import pyqtSignal
from logging import Logger

class QtPanelObserver(PanelObserver):
    robot_control_changed_signal = pyqtSignal(RobotControlData)
    camera_control_changed_signal = pyqtSignal(CameraControlData)
    def __init__(self, logger:Logger) -> None:
        super().__init__()
        self.robot_control_changed_signal = None
        self.camera_control_changed_signal = None
        self.logger = logger

    def on_robot_control_data_ready(self, robot_control_data:RobotControlData) -> None:
        if self.robot_control_changed_signal:
            self.robot_control_changed_signal.emit(robot_control_data)

    def on_camera_control_data_ready(self, camera_control_data:CameraControlData) -> None:
        if self.camera_control_changed_signal:
            self.camera_control_changed_signal.emit(camera_control_data)

    def register_robot_signal(self, signal:pyqtSignal):
        self.robot_control_changed_signal = signal

    def register_camera_signal(self, signal:pyqtSignal):
        self.camera_control_changed_signal = signal