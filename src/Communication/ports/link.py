from abc import ABC, abstractmethod
from Communication.domain.entities import WheelsModule, TelemetryMessage, TiltModule, PanModule, FocusModule
from typing import Callable

class RobotLink(ABC):
    @abstractmethod
    def send(self, wheelsModuleLeft:WheelsModule, wheelsModuleRight:WheelsModule) -> None:
        pass
    
    @abstractmethod
    def send(self, module:TiltModule) -> None:
        pass

    @abstractmethod
    def send(self, module:PanModule) -> None:
        pass

    @abstractmethod
    def send(self, module:FocusModule) -> None:
        pass

    @abstractmethod
    def callback_setup(self, callback:Callable[[TelemetryMessage], None]) -> None:
        pass

    @abstractmethod
    def start_listening(self) -> None:
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        pass