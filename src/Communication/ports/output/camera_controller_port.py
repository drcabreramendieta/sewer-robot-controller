from abc import ABC, abstractmethod
from Communication.domain.entities.camera_entities import CameraState

class CameraControllerPort(ABC):
    @abstractmethod
    def initialize_camera(self) -> None:
        pass

    @abstractmethod
    def update_camera_state(self, camera_state:CameraState) -> None:
        pass
