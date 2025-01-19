from dataclasses import dataclass
from enum import Enum, auto
"""Wheel control entities for robot movement.

This module defines the data structures and enumerations used for 
controlling the robot's wheel movements and direction.
"""

class Direction(Enum):
    """Robot movement direction states.

    Attributes:
        FORWARD: Move robot forward
        BACKWARD: Move robot backward 
        STOP: Stop robot movement
    """
    FORWARD = auto()
    BACKWARD = auto()
    STOP = auto()

class Rotation(Enum):
    """Robot rotation direction states.

    Attributes:
        LEFT: Rotate robot left
        RIGHT: Rotate robot right
        CENTER: No rotation (straight)
    """
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()

@dataclass
class WheelsModule:
    """Robot wheels state configuration.

    Attributes:
        direction (Direction): Movement direction state
        rotation (Rotation): Rotation direction state
        speed (int): Movement speed (0-100)
    """
    direction: Direction
    rotation: Rotation
    speed: int