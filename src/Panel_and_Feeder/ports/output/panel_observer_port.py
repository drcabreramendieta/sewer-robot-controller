from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData

class PanelObserverPort(ABC):
    """Abstract base class for panel control observers.

    Defines interface for objects that need to receive notifications
    about robot and camera control state changes.
    """
    @abstractmethod
    def on_robot_control_data_ready(self, robot_control_data:RobotControlData) -> None:
        """Handle notification of robot control update.

        Args:
            robot_control_data (RobotControlData): Updated robot control state

        Raises:
            ValueError: If control data is invalid
        """
        pass

    @abstractmethod
    def on_camera_control_data_ready(self, camera_control_data:CameraControlData) -> None:
        """Handle notification of camera control update.

        Args:
            camera_control_data (CameraControlData): Updated camera control state

        Raises:
            ValueError: If control data is invalid
        """
        pass
