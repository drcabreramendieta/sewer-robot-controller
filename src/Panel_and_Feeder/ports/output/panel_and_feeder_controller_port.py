from abc import ABC, abstractmethod
from typing import Callable
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData, FeederControlData
"""Abstract interface for panel and feeder hardware control.

This module defines the interface for controlling panel and feeder
hardware through callbacks and message passing.
"""
class PanelAndFeederControllerPort(ABC):
    """Abstract base class for hardware control operations.

    Defines interface for managing hardware control through callbacks 
    and message passing.
    """

    @abstractmethod
    def robot_callback_setup(self, robot_callback:Callable[[RobotControlData],None]) -> None:
        """Configure callback for robot control updates.

        Args:
            robot_callback (Callable[[RobotControlData], None]): Function to handle
                robot state updates

        Raises:
            ValueError: If callback is None or invalid
        """
        pass

    @abstractmethod
    def camera_callback_setup(self, camera_callback:Callable[[CameraControlData],None]) -> None:
        """Configure callback for camera control updates.

        Args:
            camera_callback (Callable[[CameraControlData], None]): Function to handle 
                camera state updates

        Raises:
            ValueError: If callback is None or invalid
        """
        pass

    @abstractmethod
    def feeder_callback_setup(self, feeder_callback:Callable[[FeederControlData],None]) -> None:
        """Configure callback for feeder control updates.

        Args:
            feeder_callback (Callable[[FeederControlData], None]): Function to handle
                feeder state updates

        Raises:
            ValueError: If callback is None or invalid
        """
        pass

    @abstractmethod
    def start_listening(self) -> None:
        """Start listening for hardware control updates.

        Raises:
            RuntimeError: If listening fails to start or is already running
        """
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        """Stop listening for hardware control updates.

        Raises:
            RuntimeError: If listening fails to stop or is not running
        """
        pass
    
    @abstractmethod
    def send_message(self, message:str):
        """Send control message to hardware.

        Args:
            message (str): Control command to send to hardware

        Raises:
            ValueError: If message is empty or invalid
            RuntimeError: If message sending fails
        """ 
        pass