from Communication.ports.output import WheelsControllerPort
from Communication.domain.entities.wheels_entities import WheelsModule, Direction, Rotation
import can
from logging import Logger

class CanWheelsControllerAdapter(WheelsControllerPort):
    def __init__(self, bus: can.BusABC, logger: Logger) -> None:
        self.bus = bus
        self.logger = logger

    def move(self, wheels_state:WheelsModule) -> None:
        if wheels_state.direction == Direction.FORWARD:
            if wheels_state.rotation == Rotation.CENTER:
                m1 = [1, 0, wheels_state.speed]
            elif wheels_state.rotation == Rotation.LEFT:
                m1 = [1, 1, wheels_state.speed]
            elif wheels_state.rotation == Rotation.RIGHT:
                m1 = [1, 2, wheels_state.speed]
        elif wheels_state.direction == Direction.BACKWARD:
            if wheels_state.rotation == Rotation.CENTER:
                m1 = [2, 0, wheels_state.speed]
            elif wheels_state.rotation == Rotation.LEFT:
                m1 = [2, 1, wheels_state.speed]
            elif wheels_state.rotation == Rotation.RIGHT:
                m1 = [2, 2, wheels_state.speed]
        elif wheels_state.direction == Direction.STOP:
            m1 = [0, 0, wheels_state.speed]

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
