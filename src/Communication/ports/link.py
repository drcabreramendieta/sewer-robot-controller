from abc import ABC, abstractmethod
from Communication.domain.entities import WheelsModule, Telemetry
from typing import Callable

class RobotLink(ABC):
    @abstractmethod
    def send(self, wheelsModuleLeft:WheelsModule, wheelsModuleRight:WheelsModule) -> None:
        pass

    @abstractmethod
    def callback_setup(self, callback:Callable[[Telemetry], None]) -> None:
        pass

    @abstractmethod
    def start_listening(self) -> None:
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        pass