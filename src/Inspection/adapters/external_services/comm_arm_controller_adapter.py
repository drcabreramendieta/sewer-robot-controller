from Inspection.ports.ouput.arm_controller_port import ArmControllerPort
from Communication.ports.input import ArmServicePort
from Communication.domain.entities.arm_entities import ArmState, ArmMotion
from logging import Logger

class CommArmControllerAdapter(ArmControllerPort):
    def __init__(self, arm_service:ArmServicePort, logger:Logger) -> None:
        super().__init__()
        self.arm_service = arm_service
        self.logger = logger

    def initialize_arm(self) -> None:
        self.arm_service.initialize_arm()

    def arm_up(self) -> None:
        self.arm_service.move_arm(ArmMotion.UP)

    def arm_down(self) -> None:
        self.arm_service.move_arm(ArmMotion.DOWN)

    def arm_stop(self) -> None:
        self.arm_service.move_arm(ArmMotion.STOP)
