from Communication.ports.output.camera_controller_port import CameraControllerPort
from Communication.domain.entities.camera_entities import CameraState
import can
from logging import Logger
"""Module for CAN bus communication adapter to control camera functionality.

This module provides an implementation of the CameraControllerPort interface
using CAN bus protocol for camera control operations.
"""


class CanCameraControllerAdapter(CameraControllerPort):
    """Adapter class for controlling camera operations through CAN bus.

    This class implements the CameraControllerPort interface and handles
    the communication between the application and the camera hardware
    using the CAN bus protocol.

    Args:
        bus (can.BusABC): CAN bus instance for communication
        logger (Logger): Logger instance for error and info logging

    Attributes:
        callback: Callback function for CAN message handling
        notifier: CAN bus message notifier
        bus: CAN bus instance
        logger: Logger instance
    """
    def __init__(self, bus: can.BusABC, logger: Logger) -> None:
        """Initialize the CAN camera controller adapter.

        Args:
            bus (can.BusABC): CAN bus instance for communication
            logger (Logger): Logger instance for error and info logging
        """
        self.callback = None
        self.notifier = None
        self.bus = bus
        self.logger = logger

    def initialize_camera(self) -> bool:
        """Initialize the camera through CAN bus communication.

        Sends initialization message to the camera through CAN bus.

        Returns:
            bool: True if initialization message was sent successfully

        Raises:
            can.CanError: If CAN communication fails
            OSError: If device access fails
        """
        m1 = [0x77, 0x74]
        #self.logger.info(f"Initializing camera with message: {m1}")
        try:
            message1 = can.Message(arbitration_id=0x0002, data=m1, is_extended_id=False)
            self.bus.send(message1)
            self.logger.info("Camera initialization message sent successfully")
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
        return True

    def update_camera_state(self, module: CameraState) -> None:
        """Update camera state based on focus and pan parameters.

        Translates camera state parameters into CAN bus protocol bytes
        for camera control.

        Args:
            module (CameraState): Camera state object containing focus and pan parameters

        Note:
            Focus options: 'O' (out), 'I' (in), 'S' (stop)
            Pan options: 'R' (right), 'L' (left), 'S' (stop)
        """
        if module.focus == "O":
            byte1 = 0x94
        elif module.focus == "I":
            byte1 = 0x91
        elif module.focus == "S":
            byte1 = 0x04

        if module.pan == "R":
            byte2 = 0x44
        elif module.pan == "L":
            byte2 = 0x33
        elif module.pan == "S":
            byte2 = 0x02

        if module.tilt == "U":
            byte3 = 0x11
        elif module.tilt == "D":
            byte3 = 0x22
        elif module.tilt == "S":
            byte3 = 0x01

        if 0 <= module.light < 11:
            byte4 = 0x2a
        elif 11 <= module.light < 22:
            byte4 = 0x3a
        elif 22 <= module.light < 33:
            byte4 = 0x4a
        elif 33 <= module.light < 44:
            byte4 = 0x5a
        elif 44 <= module.light < 55:
            byte4 = 0x6a
        elif 55 <= module.light < 66:
            byte4 = 0x9a
        elif 66 <= module.light < 77:
            byte4 = 0x5b
        elif 77 <= module.light < 88:
            byte4 = 0x9b
        elif 88 <= module.light <= 100:
            byte4 = 0x6c

        m1 = [byte1, byte2, byte3, byte4]

        #self.logger.info(f"Sending camera state module message: {m1}")
        try:
            message1 = can.Message(arbitration_id=0x0003, data=m1, is_extended_id=False)
            self.bus.send(message1)
            self.logger.info("Camera message sent successfully")
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
