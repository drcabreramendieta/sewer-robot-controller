from dataclasses import dataclass

@dataclass
class WheelsModule:
    side: str
    direction: str
    speed: int

@dataclass
class TelemetryMessage:
    message_type: str
    variables: dict
    timestamp : float

@dataclass
class CameraStateModule:
    initialized: bool
    tilt: str
    pan: str
    focus: str
    zoom: str
    light: int