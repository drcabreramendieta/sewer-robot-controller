from Inspection.ports.ouput.camera_controller_port import CameraControllerPort
from Communication.domain.entities.camera_entities import LightState, TiltState, PanState, ZoomState, FocusState
from Communication.ports.input import CameraServicePort
from logging import Logger

class CommCameraControllerAdapter(CameraControllerPort):
    def __init__(self, camera:CameraServicePort, logger:Logger) -> None:
        super().__init__()
        self.camera = camera
        self.logger = logger

    def tilt_up(self) -> None:
        self.camera.move_tilt(TiltState.UP)

    def tilt_down(self) -> None:
        self.camera.move_tilt(TiltState.DOWN)

    def tilt_stop(self) -> None:
        self.camera.move_tilt(TiltState.STOP)

    def pan_left(self) -> None:
        self.camera.move_pan(PanState.LEFT)

    def pan_right(self) -> None:
        self.camera.move_pan(PanState.RIGHT)

    def pan_stop(self) -> None:
        self.camera.move_pan(PanState.STOP)

    def focus_in(self) -> None:
        self.camera.change_focus(FocusState.IN)

    def focus_out(self) -> None:
        self.camera.change_focus(FocusState.OUT)

    def focus_stop(self) -> None:
        self.camera.change_focus(FocusState.STOP)
    
    def zoom_in(self) -> None:
        self.camera.change_zoom(ZoomState.IN)

    def zoom_out(self) -> None:
        self.camera.change_zoom(ZoomState.OUT)

    def zoom_stop(self) -> None:
        self.camera.change_zoom(ZoomState.STOP)


    def change_light(self, value:int) -> None:
        self.camera.change_light_level(LightState(value=value))

    def init_camera(self) -> None:
        self.camera.initialize_camera()