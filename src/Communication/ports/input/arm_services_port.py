from abc import ABC, abstractmethod
from Communication.domain.entities.arm_entities import ArmMotion


class ArmServicePort(ABC):

    @abstractmethod
    def initialize_arm(self) -> None:
        pass

    @abstractmethod
    def move_arm(self, motion: ArmMotion) -> None:
        pass