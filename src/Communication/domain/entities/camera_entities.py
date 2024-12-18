from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class LightState:
    value: int

class FocusState(Enum):
    OUT = auto()
    IN = auto()
    STOP = auto()

class PanState(Enum):
    RIGHT = auto()
    LEFT = auto()
    STOP = auto()

class TiltState(Enum):
    UP = auto()
    DOWN = auto()
    STOP = auto()

class ZoomState(Enum):
    IN = auto()
    OUT = auto()
    STOP = auto()

@dataclass
class CameraState:
    initialized: bool
    tilt: TiltState
    pan: PanState
    focus: FocusState
    zoom: ZoomState
    light: LightState