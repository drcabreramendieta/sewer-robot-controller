from Communication.application.services.movement_service import MovementService
from Communication.domain.entities.wheels_entities import WheelsModule
import can
from logging import Logger
from Inspection.ui.main_window import MainWindow
# TODO: Remove the dependency of MainWindow here

class CanWheelsControllerAdapter(MovementService):
    def __init__(self, bus: can.BusABC, logger: Logger) -> None:
        self.bus = bus
        self.logger = logger

    def move(self, wheelsModule:WheelsModule) -> None:
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
                MainWindow.show_error_dialog_restart()
            elif e.error_code == 6:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()
            else:
                self.logger.error("Unknown CAN error")
                MainWindow.show_error_dialog_restart()
        except OSError as e:
            self.logger.error(f"OSError: {e}")
            if e.errno == 19:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()