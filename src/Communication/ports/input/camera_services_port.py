from abc import ABC, abstractmethod
from Communication.domain.entities.camera_entities import LightState, TiltState, PanState, ZoomState, FocusState

class CameraServicePort(ABC):
    """Abstract interface for camera control services.

    This interface defines the required methods for implementing
    camera control functionality including movement, focus, zoom
    and lighting controls.
    """
    @abstractmethod
    def initialize_camera(self) -> None:
        """Initialize camera hardware and settings."""
        pass

    @abstractmethod
    def change_light_level(self, light_state:LightState) -> None:
        """Change camera light intensity.

        Args:
            light_state: New light level state
        """
        pass

    @abstractmethod
    def move_tilt(self, tilt_state:TiltState) -> None:
        """Control camera vertical tilt movement.

        Args:
            tilt_state: New tilt direction state
        """
        pass

    @abstractmethod
    def move_pan(self, pan_state:PanState) -> None:
        """Control camera horizontal pan movement.

        Args:
            pan_state: New pan direction state
        """
        pass

    @abstractmethod
    def change_focus(self, focus_state:FocusState) -> None:
        """Adjust camera focus.

        Args:
            focus_state: New focus state
        """
        
        pass

    @abstractmethod
    def change_zoom(self, zoom_state:ZoomState) -> None:
        """Control camera zoom level.

        Args:
            zoom_state: New zoom state
        """
        pass