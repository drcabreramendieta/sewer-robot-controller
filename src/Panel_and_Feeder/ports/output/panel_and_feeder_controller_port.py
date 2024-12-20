from abc import ABC, abstractmethod
from typing import Callable
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData, FeederControlData

class PanelAndFeederControllerPort(ABC):
    @abstractmethod
    def robot_callback_setup(self, robot_callback:Callable[[RobotControlData],None]) -> None:
        pass

    @abstractmethod
    def camera_callback_setup(self, camera_callback:Callable[[CameraControlData],None]) -> None:
        pass

    @abstractmethod
    def feeder_callback_setup(self, feeder_callback:Callable[[FeederControlData],None]) -> None:
        pass

    @abstractmethod
    def start_listening(self) -> None:
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        pass
    
    @abstractmethod
    def send_message(self, message:str): 
        pass