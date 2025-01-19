from abc import ABC, abstractmethod
"""Abstract interface for camera control operations.

This module defines the interface for controlling camera movements,
focus, and lighting in the inspection system.


"""
class CameraControllerPort(ABC):
    """Abstract base class for camera control operations.

    Defines interface for camera movement control including tilt,
    pan, focus and lighting operations.
    """
    @abstractmethod
    def tilt_up(self) -> None:
        """Move camera tilt mechanism upward.

        Raises:
            RuntimeError: If movement fails
        """      
        pass

    @abstractmethod
    def tilt_down(self) -> None:
        """Move camera tilt mechanism downward.

        Raises:
            RuntimeError: If movement fails
        """     
        pass

    @abstractmethod
    def tilt_stop(self) -> None:
        """Stop camera tilt movement.

        Raises:
            RuntimeError: If stop command fails
        """    
        pass

    @abstractmethod
    def pan_left(self) -> None:
        """Move camera pan mechanism leftward.

        Raises:
            RuntimeError: If movement fails
        """  
        pass

    @abstractmethod
    def pan_right(self) -> None:
        """Move camera pan mechanism rightward.

        Raises:
            RuntimeError: If movement fails
        """
        pass

    @abstractmethod
    def pan_stop(self) -> None:
        """Stop camera pan movement.

        Raises:
            RuntimeError: If stop command fails
        """
        pass

    @abstractmethod
    def focus_in(self) -> None:
        """Adjust camera focus closer.

        Raises:
            RuntimeError: If focus adjustment fails
        """
        pass

    @abstractmethod
    def focus_out(self) -> None:
        """Adjust camera focus farther.

        Raises:
            RuntimeError: If focus adjustment fails
        """
        pass

    @abstractmethod
    def focus_stop(self) -> None:
        """Stop camera focus adjustment.

        Raises:
            RuntimeError: If stop command fails
        """
        pass

    @abstractmethod
    def change_light(self, value:int) -> None:
        """Adjust camera light intensity.

        Args:
            value (int): Light intensity value (0-100)

        Raises:
            ValueError: If value is out of valid range
            RuntimeError: If light adjustment fails
        """
        pass

    @abstractmethod
    def init_camera(self) -> None:
        """Initialize camera system.

        Raises:
            RuntimeError: If initialization fails
            ConnectionError: If camera not connected
        """
        pass

