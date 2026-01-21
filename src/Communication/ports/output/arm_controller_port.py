from abc import ABC, abstractmethod
from Communication.domain.entities.arm_entities import ArmState


class ArmControllerPort(ABC):

    @abstractmethod
    def initialize_arm(self) -> None:
        pass

    @abstractmethod
    def update_arm_state(self, arm_state: ArmState) -> None:
        pass
