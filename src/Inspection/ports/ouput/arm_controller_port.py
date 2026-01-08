from abc import ABC, abstractmethod

class ArmControllerPort(ABC):

    @abstractmethod
    def arm_up(self) -> None:
        pass

    @abstractmethod
    def arm_down(self) -> None:
        pass

    @abstractmethod
    def arm_stop(self) -> None:
        pass
