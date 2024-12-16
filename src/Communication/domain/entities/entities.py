from dataclasses import dataclass


@dataclass
class WheelsModule:
    direction: str
    rotation: str
    speed: int

@dataclass
class TelemetryMessage:
    message_type: str
    variables: dict
    timestamp : float
