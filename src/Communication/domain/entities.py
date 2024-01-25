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
class TiltModule:
    direction: str

@dataclass
class PanModule:
    direction: str

@dataclass
class FocusModule:
    direction: str