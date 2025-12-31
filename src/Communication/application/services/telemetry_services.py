from Communication.ports.input import TelemetryServicesPort
from Communication.ports.output import TelemetryObserverPort
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Communication.ports.output import TelemetryControllerPort
from logging import Logger
from typing import List

class TelemetryServices(TelemetryServicesPort):
    observers:List[TelemetryObserverPort]
    def __init__(self, telemetry_controller:TelemetryControllerPort, logger:Logger) -> None:
        super().__init__()
        self.observers = []
        self.telemetry_controller = telemetry_controller
        self.logger = logger
        telemetry_controller.callback_setup(self._notify)

    def _notify(self, telemetry:TelemetryMessage) -> None:
        for observer in self.observers:
            observer.on_telemetry_ready(telemetry=telemetry)

    def register_observer(self, observer:TelemetryObserverPort):
        self.observers.append(observer)

    def start_listening(self):
        self.telemetry_controller.start_listening()

    def stop_listening(self):
        self.telemetry_controller.stop_listening()
