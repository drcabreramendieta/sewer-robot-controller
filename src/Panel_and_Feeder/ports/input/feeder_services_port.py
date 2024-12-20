from abc import ABC, abstractmethod
from Panel_and_Feeder.ports.output import FeederObserverPort

class FeederServicesPort(ABC):
    @abstractmethod
    def register_observer(self, observer:FeederObserverPort):
        pass

    @abstractmethod
    def start_listening(self):
        pass

    @abstractmethod
    def stop_listening(self):
        pass

    @abstractmethod
    def send_message(self, message:str):
        pass