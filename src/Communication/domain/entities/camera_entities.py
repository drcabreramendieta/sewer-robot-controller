from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class LightState:
    """Camera light intensity state.

    Attributes:
        value (int): Light intensity level (0-100)
    """
    value: int

class FocusState(Enum):
    """Camera focus control states.

    Attributes:
        OUT: Move focus outward
        IN: Move focus inward
        STOP: Stop focus movement
    """
    OUT = auto()
    IN = auto()
    STOP = auto()

class PanState(Enum):
    """Camera horizontal pan control states.

    Attributes:
        RIGHT: Pan camera right
        LEFT: Pan camera left
        STOP: Stop pan movement
    """
    RIGHT = auto()
    LEFT = auto()
    STOP = auto()

class TiltState(Enum):
    """Camera vertical tilt control states.

    Attributes:
        UP: Tilt camera upward
        DOWN: Tilt camera downward
        STOP: Stop tilt movement
    """
    UP = auto()
    DOWN = auto()
    STOP = auto()

class ZoomState(Enum):
    """Camera zoom control states.

    Attributes:
        IN: Zoom in (telephoto)
        OUT: Zoom out (wide)
        STOP: Stop zoom movement
    """
    IN = auto()
    OUT = auto()
    STOP = auto()

@dataclass
class CameraState:
    """Complete camera state representation.

    Attributes:
        initialized (bool): Whether camera is initialized
        tilt (TiltState): Current vertical tilt state
        pan (PanState): Current horizontal pan state
        focus (FocusState): Current focus state
        zoom (ZoomState): Current zoom state
        light (LightState): Current light intensity state
    """
    initialized: bool
    tilt: TiltState
    pan: PanState
    focus: FocusState
    zoom: ZoomState
    light: LightState