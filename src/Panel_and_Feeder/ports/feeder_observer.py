from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities import FeederControlData

class FeederObserver(ABC):
    @abstractmethod
    def on_feeder_control_data_ready(self, feeder_control_data:FeederControlData) -> None:
        pass
