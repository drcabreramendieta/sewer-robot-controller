from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData, ArmControlData

class PanelUpdateServicesPort(ABC):
    @abstractmethod
    def update_robot_control(self, robot_control_data:RobotControlData) -> None:
        pass

    @abstractmethod
    def update_robot_speed(self, speed:int):
        pass

    @abstractmethod
    def update_camera_control(self, camera_control_data:CameraControlData) -> None:
        pass

    @abstractmethod
    def update_arm_control(self, arm_control_data: ArmControlData) -> None:
        pass

    @abstractmethod
    def update_camera_light(self, light:int):
        pass

    @abstractmethod
    def set_expansion_mode(self, is_enabled: bool) -> None:
        pass
