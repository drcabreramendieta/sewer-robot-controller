from Communication.ports.input import CameraServicePort
from Communication.ports.output import CameraControllerPort
from Communication.domain.entities.camera_entities import LightState, TiltState, PanState, ZoomState, FocusState, CameraState
from dependency_injector.providers import Provider

class CameraServices(CameraServicePort):
    def __init__(self, camera_controller: Provider[CameraControllerPort]) -> None:
        super().__init__()
        self.camera = CameraState(initialized=False, 
                                  tilt=TiltState.STOP,
                                  pan=PanState.STOP,
                                  focus=FocusState.STOP,
                                  zoom=ZoomState.STOP,
                                  light=LightState(value=0))
        self._camera_controller_provider = camera_controller

    def _controller(self) -> CameraControllerPort:
        return self._camera_controller_provider()

    def initialize_camera(self) -> None:
        self._controller().initialize_camera()

    def change_light_level(self, light_state:LightState) -> None:
        self.camera.light = light_state
        self._controller().update_camera_state(self.camera)

    def move_tilt(self, tilt_state: TiltState) -> None:
        self.camera.tilt = tilt_state
        self.camera.pan = PanState.STOP
        self.camera.focus = FocusState.STOP
        self.camera.zoom = ZoomState.STOP
        self._controller().update_camera_state(self.camera)

    def move_pan(self, pan_state: PanState) -> None:
        self.camera.pan = pan_state
        self.camera.tilt = TiltState.STOP
        self.camera.focus = FocusState.STOP
        self.camera.zoom = ZoomState.STOP
        self._controller().update_camera_state(self.camera)

    def change_focus(self, focus_state: FocusState) -> None:
        self.camera.focus = focus_state
        self.camera.tilt = TiltState.STOP
        self.camera.pan = PanState.STOP
        self.camera.zoom = ZoomState.STOP
        self._controller().update_camera_state(self.camera)

    def change_zoom(self, zoom_state: ZoomState) -> None:
        self.camera.zoom = zoom_state
        self.camera.tilt = TiltState.STOP
        self.camera.pan = PanState.STOP
        self.camera.focus = FocusState.STOP
        self._controller().update_camera_state(self.camera)
