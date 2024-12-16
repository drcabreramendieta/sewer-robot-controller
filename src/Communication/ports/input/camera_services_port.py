from abc import ABC, abstractmethod
from Communication.domain.entities.camera_entities import LightState, TiltState, PanState, ZoomState, FocusState

class CameraServicePort(ABC):
    @abstractmethod
    def initialize_camera(self) -> None:
        pass

    @abstractmethod
    def change_light_level(self, light_state:LightState) -> None:
        pass

    @abstractmethod
    def move_tilt(self, tilt_state:TiltState) -> None:
        pass

    @abstractmethod
    def move_pan(self, pan_state:PanState) -> None:
        pass

    @abstractmethod
    def change_focus(self, focus_state:FocusState) -> None:
        pass

    @abstractmethod
    def change_zoom(self, zoom_state:ZoomState) -> None:
        pass