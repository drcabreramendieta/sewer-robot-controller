from logging import Logger
from typing import Callable, Optional

from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import (
    CameraControlData,
    FeederControlData,
    RobotControlData,
    SerialConfig,
)
from Panel_and_Feeder.ports.output.panel_and_feeder_controller_port import (
    PanelAndFeederControllerPort,
)


class MockSerialPanelAndFeederControllerAdapter(PanelAndFeederControllerPort):
    def __init__(self, serial_conf: SerialConfig, logger: Logger) -> None:
        super().__init__()
        self.serial_conf = serial_conf
        self.logger = logger
        self.robot_callback: Optional[Callable[[RobotControlData], None]] = None
        self.camera_callback: Optional[Callable[[CameraControlData], None]] = None
        self.feeder_callback: Optional[Callable[[FeederControlData], None]] = None
        self.running = False

    def robot_callback_setup(self, robot_callback: Callable[[RobotControlData], None]) -> None:
        self.robot_callback = robot_callback

    def camera_callback_setup(self, camera_callback: Callable[[CameraControlData], None]) -> None:
        self.camera_callback = camera_callback

    def feeder_callback_setup(self, feeder_callback: Callable[[FeederControlData], None]) -> None:
        self.feeder_callback = feeder_callback

    def start_listening(self) -> None:
        self.running = True
        self.logger.info("Mock serial start_listening")

    def stop_listening(self) -> None:
        self.running = False
        self.logger.info("Mock serial stop_listening")

    def send_message(self, message: str):
        self.logger.info("Mock serial send: %s", message)
