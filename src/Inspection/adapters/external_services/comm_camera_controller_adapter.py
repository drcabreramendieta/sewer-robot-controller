from Inspection.ports.ouput.camera_controller_port import CameraControllerPort
from Communication.domain.entities.camera_entities import LightState, TiltState, PanState, ZoomState, FocusState
from Communication.ports.input import CameraServicePort
from logging import Logger
"""Communication adapter for camera controller implementation.

This module provides an adapter that implements the CameraControllerPort interface
using the Communication service layer for camera control operations.
"""
class CommCameraControllerAdapter(CameraControllerPort):
    """Adapter for camera control through Communication service.

    Args:
        camera (CameraServicePort): Camera service for control operations
        logger (Logger): Logger instance for error and info logging

    Attributes:
        camera: Camera service instance
        logger: Logger instance
    """

    def __init__(self, camera:CameraServicePort, logger:Logger) -> None:
        """Initialize camera controller adapter."""
        super().__init__()
        self.camera = camera
        self.logger = logger

    def tilt_up(self) -> None:
        """Move camera tilt upward."""
        self.camera.move_tilt(TiltState.UP)

    def tilt_down(self) -> None:
        """Move camera tilt downward."""
        self.camera.move_tilt(TiltState.DOWN)

    def tilt_stop(self) -> None:
        """Stop camera tilt movement."""
        self.camera.move_tilt(TiltState.STOP)

    def pan_left(self) -> None:
        """Pan camera to the left."""
        self.camera.move_pan(PanState.LEFT)

    def pan_right(self) -> None:
        """Pan camera to the right."""
        self.camera.move_pan(PanState.RIGHT)

    def pan_stop(self) -> None:
        """Stop camera pan movement."""
        self.camera.move_pan(PanState.STOP)

    def focus_in(self) -> None:
        """Move camera focus inward."""
        self.camera.change_focus(FocusState.IN)

    def focus_out(self) -> None:
        """Move camera focus outward."""
        self.camera.change_focus(FocusState.OUT)

    def focus_stop(self) -> None:
        """Stop camera focus movement."""
        self.camera.change_focus(FocusState.STOP)

    def change_light(self, value:int) -> None:
        """Change camera light intensity.

        Args:
            value: Light intensity level (0-100)
        """
        self.camera.change_light_level(LightState(value=value))

    def init_camera(self) -> None:
        
        self.camera.initialize_camera()