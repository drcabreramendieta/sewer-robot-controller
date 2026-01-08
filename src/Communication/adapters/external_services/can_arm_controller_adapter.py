from Communication.ports.output.arm_controller_port import ArmControllerPort
from Communication.domain.entities.arm_entities import ArmState, ArmMotion

import can
from logging import Logger


class CanArmControllerAdapter(ArmControllerPort):
    """
    Adapter CAN para control del brazo (UP / DOWN / STOP),
    siguiendo el mismo estilo del CanCameraControllerAdapter.
    """

    ARM_ARBITRATION_ID = 0x0004

    ARM_UP_BYTES = [0x08]
    ARM_DOWN_BYTES = [0x10]
    ARM_STOP_BYTES = [0x00]

    def __init__(self, bus: can.BusABC, logger: Logger) -> None:
        self.callback = None
        self.notifier = None
        self.bus = bus
        self.logger = logger

    def update_arm_state(self, arm_state: ArmState) -> None:
        """
        Envía comando del brazo según arm_state.motion (UP/DOWN/STOP).
        """
        if arm_state.motion == ArmMotion.UP:
            data = self.ARM_UP_BYTES
        elif arm_state.motion == ArmMotion.DOWN:
            data = self.ARM_DOWN_BYTES
        else:
            data = self.ARM_STOP_BYTES

        try:
            message = can.Message(
                arbitration_id=self.ARM_ARBITRATION_ID,
                data=data,
                is_extended_id=False
            )
            self.bus.send(message)
            self.logger.info(f"Arm command sent: {arm_state.motion.name}")

        except can.CanError as e:
            self.logger.error(f"CAN Error: {e}")
            if getattr(e, "error_code", None) == 100:
                self.logger.error("Network is down")
            elif getattr(e, "error_code", None) == 6:
                self.logger.error("No such device or address")
            else:
                self.logger.error("Unknown CAN error")

        except OSError as e:
            self.logger.error(f"OSError: {e}")
            if getattr(e, "errno", None) == 19:
                self.logger.error("No such device or address")
