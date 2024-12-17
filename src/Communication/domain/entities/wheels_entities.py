from dataclasses import dataclass
from enum import Enum, auto

class Direction(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    STOP = auto()

class Rotation(Enum):
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()

@dataclass
class WheelsModule:
    direction: Direction
    rotation: Rotation
    speed: int