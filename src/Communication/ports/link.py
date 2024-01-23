from abc import ABC, abstractmethod
from Communication.domain.entities import WheelsModule

class RobotLink(ABC):
    @abstractmethod
    def send(self, wheelsModuleLeft:WheelsModule, wheelsModuleRight:WheelsModule) -> None:
        pass