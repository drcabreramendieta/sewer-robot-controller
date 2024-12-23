from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData

class FeederUpdateServicePort(ABC):
    @abstractmethod
    def update_feeder_control(self, feeder_control_data:FeederControlData) -> None:
        pass

    @abstractmethod
    def send_message(self, msg:str) -> None:
        pass