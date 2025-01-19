from Communication.ports.output import WheelsControllerPort
from Communication.domain.entities.wheels_entities import WheelsModule
import can
from logging import Logger

"""CAN bus communication adapter for wheels control.

This module provides an implementation of the WheelsControllerPort interface 
using CAN bus protocol for controlling robot wheel movements.
"""


class CanWheelsControllerAdapter(WheelsControllerPort):
    """Adapter for controlling robot wheels through CAN bus.

    This class implements the WheelsControllerPort interface and manages
    the communication between the application and wheel control systems
    using the CAN bus protocol.

    Args:
        bus (can.BusABC): CAN bus instance for communication
        logger (Logger): Logger instance for error and info logging

    Attributes:
        bus: CAN bus instance
        logger: Logger instance
    """
    
    def __init__(self, bus: can.BusABC, logger: Logger) -> None:
        """Initialize the CAN wheels controller adapter.

        Args:
            bus (can.BusABC): CAN bus instance for communication
            logger (Logger): Logger instance for error and info logging
        """
        self.bus = bus
        self.logger = logger

    def move(self, wheelsModule:WheelsModule) -> None:
        """Send movement commands to the robot wheels.

        Args:
            wheelsModule (WheelsModule): Contains movement parameters:
                direction: 'F' (forward), 'B' (backward), 'S' (stop)
                rotation: 'N' (none), 'L' (left), 'R' (right)
                speed: Movement speed value

        Raises:
            can.CanError: If CAN communication fails
            OSError: If device access fails
        """
        if wheelsModule.direction == "F":
            if wheelsModule.rotation == "N":
                m1 = [1, 0, wheelsModule.speed]
            elif wheelsModule.rotation == "L":
                m1 = [1, 1, wheelsModule.speed]
            elif wheelsModule.rotation == "R":
                m1 = [1, 2, wheelsModule.speed]
        elif wheelsModule.direction == "B":
            if wheelsModule.rotation == "N":
                m1 = [2, 0, wheelsModule.speed]
            elif wheelsModule.rotation == "L":
                m1 = [2, 1, wheelsModule.speed]
            elif wheelsModule.rotation == "R":
                m1 = [2, 2, wheelsModule.speed]
        elif wheelsModule.direction == "S":
            m1 = [0, 0, wheelsModule.speed]

        #self.logger.info(f"Sending wheels module message: {m1}")
        try:
            message1 = can.Message(arbitration_id=0x0001, data=m1, is_extended_id=False)
            self.bus.send(message1)
            self.logger.info("Robot message sent successfully")
        except can.CanError as e:
            self.logger.error(f"CAN Error: {e}")
            if e.error_code == 100:  # Network is down
                self.logger.error("Network is down")
            elif e.error_code == 6:  # No such device or address
                self.logger.error("No such device or address")
            else:
                self.logger.error("Unknown CAN error")
        except OSError as e:
            self.logger.error(f"OSError: {e}")
            if e.errno == 19:  # No such device or address
                self.logger.error("No such device or address")