from abc import ABC, abstractmethod
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from typing import Callable

class TelemetryControllerPort(ABC):
    @abstractmethod
    def callback_setup(self, callback: Callable[[TelemetryMessage], None]) -> None:
        pass

    @abstractmethod
    def start_listening(self) -> None:
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        pass