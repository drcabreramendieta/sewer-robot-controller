from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities import RobotControlData, CameraControlData

class PanelObserver(ABC):
    @abstractmethod
    def on_robot_control_data_ready(self, robot_control_data:RobotControlData) -> None:
        pass

    @abstractmethod
    def on_camera_control_data_ready(self, camera_control_data:CameraControlData) -> None:
        pass
