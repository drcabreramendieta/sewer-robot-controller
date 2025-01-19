from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData
"""Abstract interface for panel update services.

This module defines the interface for services that manage robot movement
and camera control operations.

"""
class PanelUpdateServicesPort(ABC):
    """Abstract base class for panel update services.

    Defines interface for managing robot movement and camera controls.
    Implementations must provide methods for updating robot movement,
    speed, camera position and lighting.
    """
    @abstractmethod
    def update_robot_control(self, robot_control_data:RobotControlData) -> None:
        """Update robot movement direction.

        Args:
            robot_control_data (RobotControlData): New movement parameters

        Raises:
            ValueError: If control data is invalid
        """
        pass

    abstractmethod
    def update_robot_speed(self, speed:int):
        """Update robot movement speed.

        Args:
            speed (int): New speed value (3-1000)

        Raises:
            ValueError: If speed is out of valid range
        """
        pass

    @abstractmethod
    def update_camera_control(self, camera_control_data:CameraControlData) -> None:
        """Update camera position and focus.

        Args:
            camera_control_data (CameraControlData): New camera parameters

        Raises:
            ValueError: If control data is invalid
        """
        pass

    abstractmethod
    def update_camera_light(self, light:int):
        """Update camera light intensity.

        Args:
            light (int): New light intensity value (0-100)

        Raises:
            ValueError: If light value is out of valid range
        """
        pass