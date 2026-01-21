from Communication.ports.output.arm_controller_port import ArmControllerPort

class MockArmControllerAdapter(ArmControllerPort):
    def initialize_arm(self) -> None:
        return

    def update_arm_state(self, state) -> None:
        return

    def arm_up(self) -> None:
        return

    def arm_down(self) -> None:
        return

    def arm_stop(self) -> None:
        return
