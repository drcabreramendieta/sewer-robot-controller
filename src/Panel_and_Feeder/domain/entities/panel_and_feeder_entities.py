from dataclasses import dataclass

@dataclass
class RobotControlData:
    direction: str

@dataclass
class CameraControlData:
    movement :str
    light: str

@dataclass
class ArmControlData:
    movement: str  # "UP", "DOWN", "STOP"
    
@dataclass
class FeederControlData:
    distance: str
    reset: str

@dataclass
class SerialConfig:
    port: str
    baudrate: int
    timeout: float

