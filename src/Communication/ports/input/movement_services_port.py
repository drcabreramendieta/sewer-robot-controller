from abc import ABC, abstractmethod
from Communication.domain.entities.wheels_entities import Direction, Rotation

class MovementServicePort(ABC):
    @abstractmethod
    def move(self, direction:Direction, rotation:Rotation, speed:int) -> None:
        pass