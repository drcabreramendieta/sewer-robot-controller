from dataclasses import dataclass
"""Panel and feeder control data entities.

This module defines the data structures for robot movement,
camera control, feeder operations and serial configuration.
"""

@dataclass
class RobotControlData:
    """Robot movement control parameters.

    Stores direction command for robot movement control.
    """
    direction: str

@dataclass
class CameraControlData:
    """Camera operation parameters.

    Stores camera movement and lighting control values.

    Attributes:
        movement (str): Camera movement command.
        light (str): Light intensity value 
    """
    movement :str
    light: str

@dataclass
class FeederControlData:
    """Feeder operation parameters.

    Stores feeder distance and reset control values.

    Attributes:
        distance (str): Feed distance value 
        reset (str): Reset state
    """
    distance: str
    reset: str

@dataclass
class SerialConfig:
    """Serial communication configuration.

    Stores serial port connection parameters.

    Attributes:
        port (str): Serial port identifier 
        baudrate (int): Communication speed 
        timeout (float): Read timeout in seconds
    """
    port: str
    baudrate: int
    timeout: float