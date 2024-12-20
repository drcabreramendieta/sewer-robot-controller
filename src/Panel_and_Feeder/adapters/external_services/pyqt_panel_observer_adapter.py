from Panel_and_Feeder.ports.output import PanelObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData

from Inspection.ports.input import PanelUpdateServicesPort
from PyQt6.QtCore import pyqtSignal, QObject
from logging import Logger

class PyqtPanelObserverAdapter(PanelObserverPort):
    def __init__(self, panel_update_services:PanelUpdateServicesPort, logger:Logger) -> None:
        super().__init__()
        self.panel_update_services = panel_update_services
        self.logger = logger
        self.pyqt_signal_connect = PyqtSignalConnect(self.panel_update_services)

    def on_robot_control_data_ready(self, robot_control_data:RobotControlData) -> None:
        if self.pyqt_signal_connect.robot_control_updated_signal:
            self.pyqt_signal_connect.robot_control_updated_signal.emit(robot_control_data)
    
    def on_camera_control_data_ready(self, camera_control_data:CameraControlData) -> None:
        if self.pyqt_signal_connect.camera_control_updated_signal:
            self.pyqt_signal_connect.camera_control_updated_signal.emit(camera_control_data)

class PyqtSignalConnect(QObject):
    robot_control_updated_signal = pyqtSignal(RobotControlData)
    camera_control_updated_signal = pyqtSignal(CameraControlData)
    def __init__(self, panel_update_services:PanelUpdateServicesPort) -> None:
        super().__init__()
        self.panel_update_services = panel_update_services
        self.robot_control_updated_signal.connect(self.panel_update_services.update_robot_control)
        self.camera_control_updated_signal.connect(self.panel_update_services.update_camera_control)