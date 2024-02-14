from abc import ABC, abstractmethod
from Communication.domain.entities import WheelsModule, TelemetryMessage, CameraStateModule
from typing import Callable
from multipledispatch import dispatch

class RobotLink(ABC):
    @abstractmethod
    def initialize_camera(self, camera_state:CameraStateModule) -> bool:
        pass

    @dispatch(WheelsModule)
    @abstractmethod
    def send(self, wheelModule:WheelsModule) -> None:
        pass
    
    @dispatch(CameraStateModule)
    @abstractmethod
    def send(self, module:CameraStateModule) -> None:
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