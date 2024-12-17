from abc import ABC, abstractmethod
from Communication.domain.entities.wheels_entities import WheelsModule

class WheelsControllerPort(ABC):
    @abstractmethod
    def move(self, wheels_state:WheelsModule) -> None:
        pass
