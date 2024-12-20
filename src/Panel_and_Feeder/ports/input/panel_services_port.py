from abc import ABC, abstractmethod
from Panel_and_Feeder.ports.output import PanelObserverPort

class PanelServicesPort(ABC):
    @abstractmethod
    def register_observer(self, observer:PanelObserverPort):
        pass

    @abstractmethod
    def start_listening(self):
        pass

    @abstractmethod
    def stop_listening(self):
        pass