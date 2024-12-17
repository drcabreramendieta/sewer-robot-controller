from abc import ABC, abstractmethod
from Communication.ports.output import TelemetryObserverPort

class TelemetryServicesPort(ABC):
    @abstractmethod
    def register_observer(self, observer:TelemetryObserverPort):
        pass

    @abstractmethod
    def start_listening(self) -> None:
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        pass