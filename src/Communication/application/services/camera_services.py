from Communication.ports.input import CameraServicePort
from 
from Communication.domain.entities.camera_entities import LightState, TiltState, PanState, ZoomState, FocusState

class CameraServices(CameraServicePort):
    def initialize_camera(self) -> None:
        pass

    def change_light_level(self, light_state:LightState) -> None:
        pass

    def move_tilt(self, tilt_state:TiltState) -> None:
        pass

    def move_pan(self, pan_state:PanState) -> None:
        pass

    def change_focus(self, focus_state:FocusState) -> None:
        pass

    def change_zoom(self, zoom_state:ZoomState) -> None:
        pass