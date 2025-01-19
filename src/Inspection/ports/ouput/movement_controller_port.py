from abc import ABC, abstractmethod
"""Abstract interface for robot movement control.

This module defines the interface for controlling robot movements
including directional control and speed adjustment.


"""
class MovementControllerPort(ABC):
    """Abstract base class for robot movement control.
    
    Defines interface for controlling robot movement operations
    including direction control and speed adjustments.
    """
    @abstractmethod
    def move_forward(self) -> None:
        """Move robot forward.

        Raises:
            RuntimeError: If movement fails
        """
        pass
    
    @abstractmethod
    def move_backward(self) -> None:
        """Move robot backward.

        Raises:
            RuntimeError: If movement fails
        """
        pass
    
    @abstractmethod
    def rotate_left_forward(self) -> None:
        """Rotate robot left while moving forward.

        Raises:
            RuntimeError: If movement fails
        """
        pass
    
    @abstractmethod
    def rotate_right_forward(self) -> None:
        """Rotate robot right while moving forward.

        Raises:
            RuntimeError: If movement fails
        """
        pass

    @abstractmethod
    def rotate_left_backward(self) -> None:
        """Rotate robot left while moving backward.

        Raises:
            RuntimeError: If movement fails
        """
        pass

    @abstractmethod
    def rotate_right_backward(self) -> None:
        """Rotate robot right while moving backward.

        Raises:
            RuntimeError: If movement fails
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop all robot movement.

        Raises:
            RuntimeError: If stop command fails
        """
        pass

    @abstractmethod
    def change_speed(self, value:int) -> None:
        """Change robot movement speed.

        Args:
            value (int): Speed value (1-3)

        Raises:
            ValueError: If speed value is out of valid range
            RuntimeError: If speed change fails
        """ 
        pass 

