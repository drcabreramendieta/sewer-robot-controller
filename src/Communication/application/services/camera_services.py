from Communication.ports.input import CameraServicePort
from Communication.ports.output import CameraControllerPort
from Communication.domain.entities.camera_entities import LightState, TiltState, PanState, ZoomState, FocusState, CameraState

class CameraServices(CameraServicePort):
    def __init__(self, camera_controller:CameraControllerPort):
        super().__init__()
        self.camera = CameraState(initialized=False, 
                                  tilt=TiltState.STOP,
                                  pan=PanState.STOP,
                                  focus=FocusState.STOP,
                                  zoom=ZoomState.STOP,
                                  light=LightState.ONE)
        self.camera_controller = camera_controller

    def initialize_camera(self) -> None:
        self.camera_controller.initialize_camera()

    def change_light_level(self, light_state:LightState) -> None:
        self.camera.light = light_state
        self.camera_controller.update_camera_state(self.camera)

    def move_tilt(self, tilt_state:TiltState) -> None:
        self.camera.tilt = tilt_state
        self.camera_controller.update_camera_state(self.camera)

    def move_pan(self, pan_state:PanState) -> None:
        self.camera.pan = pan_state
        self.camera_controller.update_camera_state(self.camera)

    def change_focus(self, focus_state:FocusState) -> None:
        self.camera.focus = focus_state
        self.camera_controller.update_camera_state(self.camera)

    def change_zoom(self, zoom_state:ZoomState) -> None:
        self.camera.zoom = zoom_state
        self.camera_controller.update_camera_state(self.camera)