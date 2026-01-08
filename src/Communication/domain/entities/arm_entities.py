from dataclasses import dataclass
from enum import Enum


class ArmMotion(Enum):
    UP = "UP"
    DOWN = "DOWN"
    STOP = "STOP"

@dataclass
class ArmState:
    initialized: bool
    motion: ArmMotion