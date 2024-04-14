from dataclasses import dataclass

@dataclass
class RobotControlData:
    speed: str
    direction: str

@dataclass
class CameraControlData:
    pan: str
    tilt: str
    light: str

@dataclass
class FeederControlData:
    speed: str
    direction: str

@dataclass
class SerialConfig:
    port: str
    baudrate: int
    timeout: float