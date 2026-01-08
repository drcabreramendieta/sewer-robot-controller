from Communication.ports.input.arm_services_port import ArmServicePort
from Communication.ports.output.arm_controller_port import ArmControllerPort
from Communication.domain.entities.arm_entities import ArmState, ArmMotion


class ArmServices(ArmServicePort):
    def __init__(self, arm_controller: ArmControllerPort):
        super().__init__()
        self.arm = ArmState(initialized=False, motion=ArmMotion.STOP)
        self.arm_controller = arm_controller

    def initialize_arm(self) -> None:
        self.arm.initialized = True
        self.arm_controller.initialize_arm()

    def move_arm(self, motion: ArmMotion) -> None:
        self.arm.motion = motion
        self.arm_controller.update_arm_state(self.arm)
