from abc import ABC, abstractmethod
from Communication.domain.entities.camera_entities import CameraState
"""Camera controller port interface definition.

This module defines the abstract interface for camera hardware control,
providing methods for initialization and state updates.
"""

class CameraControllerPort(ABC):
    """Abstract interface for camera hardware control.

    This interface defines the required methods for implementing
    low-level camera control functionality.
    """
    @abstractmethod
    def initialize_camera(self) -> None:
        """Initialize camera hardware.

        Returns:
            None
        """
        pass

    @abstractmethod
    def update_camera_state(self, camera_state:CameraState) -> None:
        """Update camera hardware state.

        Args:
            camera_state: New camera state configuration

        Returns:
            None
        """
        pass
