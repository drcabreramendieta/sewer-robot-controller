from Panel_and_Feeder.ports.input import PanelServicesPort
from Panel_and_Feeder.ports.output.panel_observer_port import PanelObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData
from Panel_and_Feeder.ports.output.panel_and_feeder_controller_port import PanelAndFeederControllerPort
from logging import Logger
from typing import List
"""Panel control services implementation.

This module provides services for managing panel operations including
robot movement and camera control with observer notifications.

"""
class PanelServices(PanelServicesPort):
    """Service for managing panel operations and notifications.

    Implements panel control services including observer pattern for
    robot and camera updates.

    Args:
        paf_controller (PanelAndFeederControllerPort): Hardware controller
        logger (Logger): Logger instance for operations
        observer (PanelObserverPort): Initial observer for updates

    Attributes:
        observers (List[PanelObserverPort]): List of registered observers
        paf_controller (PanelAndFeederControllerPort): Hardware interface
        logger (Logger): Operations logger
    """
    observers:List[PanelObserverPort]
    def __init__(self, paf_controller:PanelAndFeederControllerPort, logger:Logger, observer:PanelObserverPort) -> None:
        """Initialize panel services.

        Args:
            paf_controller (PanelAndFeederControllerPort): Hardware controller
            logger (Logger): Logger for operations
            observer (PanelObserverPort): Initial update observer

        Raises:
            ValueError: If controller or logger is None
        """
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer)
        self.paf_controller = paf_controller
        self.logger = logger
        self.paf_controller.robot_callback_setup(self._notify_robot_control_data)
        self.paf_controller.camera_callback_setup(self._notify_camera_control_data)
        super().__init__()

    def _notify_robot_control_data(self, robot_control_data:RobotControlData) -> None:
        """Notify observers of robot control updates.

        Args:
            robot_control_data (RobotControlData): Updated robot state

        Raises:
            RuntimeError: If notification fails
        """
        for observer in self.observers:
            observer.on_robot_control_data_ready(robot_control_data=robot_control_data)

    def _notify_camera_control_data(self, camera_control_data:CameraControlData) -> None:
        """Notify observers of camera control updates.

        Args:
            camera_control_data (CameraControlData): Updated camera state

        Raises:
            RuntimeError: If notification fails
        """
        for observer in self.observers:
            observer.on_camera_control_data_ready(camera_control_data=camera_control_data)

    def register_observer(self, observer:PanelObserverPort):
        """Register new observer for panel updates.

        Args:
            observer (PanelObserverPort): Observer to receive updates

        Raises:
            ValueError: If observer is None
        """
        self.observers.append(observer)

    def start_listening(self):
        """Start listening for panel control updates.

        Raises:
            RuntimeError: If listening fails to start
        """
        print('start')
        self.paf_controller.start_listening()

    def stop_listening(self):
        """Stop listening for panel control updates.

        Raises:
            RuntimeError: If listening fails to stop
        """
        self.paf_controller.stop_listening()