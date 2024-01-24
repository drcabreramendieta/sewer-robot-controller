from dataclasses import dataclass

@dataclass
class WheelsModule:
    side: str
    direction: str
    speed: int

@dataclass
class WheelInformation:
    speed: int
    temperature: int

@dataclass
class Telemetry:
    tilt: int
    temperature: int
    wheels: list[WheelInformation]

@dataclass
class TelemetryMessage:
    message_type: str
    variables: dict
    timestamp : float
