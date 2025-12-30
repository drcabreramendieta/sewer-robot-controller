from logging import Logger

from Communication.domain.entities.camera_entities import CameraState
from Communication.ports.output.camera_controller_port import CameraControllerPort


class MockCanCameraControllerAdapter(CameraControllerPort):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def initialize_camera(self) -> None:
        self.logger.info("Mock camera initialize")

    def update_camera_state(self, camera_state: CameraState) -> None:
        self.logger.info("Mock camera update: %s", camera_state)
