from Communication.ports.input import CameraServicePort
from Communication.ports.output import CameraControllerPort
from Communication.domain.entities.camera_entities import LightState, TiltState, PanState, ZoomState, FocusState, CameraState

class CameraServices(CameraServicePort):
    """Service class for managing camera operations.

    This class implements the CameraServicePort interface and provides
    methods to control various camera functions through a camera controller.

    Args:
        camera_controller (CameraControllerPort): Controller for camera operations

    Attributes:
        camera (CameraState): Current state of the camera
        camera_controller: Interface to control camera hardware
    """
    def __init__(self, camera_controller:CameraControllerPort):
        """Initialize camera services with default state."""
        super().__init__()
        self.camera = CameraState(initialized=False, 
                                  tilt=TiltState.STOP,
                                  pan=PanState.STOP,
                                  focus=FocusState.STOP,
                                  zoom=ZoomState.STOP,
                                  light=LightState(value=0))
        self.camera_controller = camera_controller

    def initialize_camera(self) -> None:
        """Initialize the camera hardware."""
        self.camera_controller.initialize_camera()

    def change_light_level(self, light_state:LightState) -> None:
        """Update camera light intensity.

        Args:
            light_state: New light level state
        """
        self.camera.light = light_state
        self.camera_controller.update_camera_state(self.camera)

    def move_tilt(self, tilt_state:TiltState) -> None:
        """Control camera tilt movement.

        Args:
            tilt_state: New tilt direction state
        """
        self.camera.tilt = tilt_state
        self.camera_controller.update_camera_state(self.camera)

    def move_pan(self, pan_state:PanState) -> None:
        """Control camera pan movement.

        Args:
            pan_state: New pan direction state
        """
        self.camera.pan = pan_state
        self.camera_controller.update_camera_state(self.camera)

    def change_focus(self, focus_state:FocusState) -> None:
        """Adjust camera focus.

        Args:
            focus_state: New focus state
        """
        self.camera.focus = focus_state
        self.camera_controller.update_camera_state(self.camera)

    def change_zoom(self, zoom_state:ZoomState) -> None:
        """Control camera zoom level.

        Args:
            zoom_state: New zoom state
        """
        self.camera.zoom = zoom_state
        self.camera_controller.update_camera_state(self.camera)