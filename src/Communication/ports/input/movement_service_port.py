from abc import ABC, abstractmethod
from Communication.domain.entities.wheels_entities import Direction, Rotation
"""Movement service port interface definition.

This module defines the abstract interface for robot movement control services,
providing methods for controlling wheel direction, rotation and speed.
"""


class MovementServicePort(ABC):
    """Abstract interface for robot movement control services.

    This interface defines the required methods for implementing
    robot movement control functionality.
    """
    @abstractmethod
    def move(self, direction:Direction, rotation:Rotation, speed:int) -> None:
        """Control robot movement parameters.

        Args:
            direction: Movement direction (FORWARD, BACKWARD, STOP)
            rotation: Rotation direction (LEFT, RIGHT, CENTER)
            speed: Movement speed value (0-100)
        """
        pass