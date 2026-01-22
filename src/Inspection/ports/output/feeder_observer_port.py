from abc import ABC, abstractmethod
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData

class FeederObserverPort(ABC):
    @abstractmethod
    def on_feeder_ready(self, feeder_control_data:FeederControlData) -> None:
        pass