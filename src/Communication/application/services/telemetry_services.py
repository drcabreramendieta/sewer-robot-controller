from Communication.ports.input import TelemetryServicesPort
from Communication.ports.output import TelemetryObserverPort
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Communication.ports.output import TelemetryControllerPort
from logging import Logger

class TelemetryServices(TelemetryServicesPort):
    def __init__(self, telemetry_controller:TelemetryControllerPort, logger:Logger, telemetry_observers:list[TelemetryObserverPort]|None=None) -> None:
        self.telemetry_observers = telemetry_observers if telemetry_observers else [] 
        self.telemetry_controller = telemetry_controller
        self.logger = logger
        telemetry_controller.callback_setup(self._notify)

    def _notify(self, telemetry:TelemetryMessage) -> None:
        for observer in self.telemetry_observers:
            observer.on_telemetry_ready(telemetry=telemetry)

    def register_observer(self, observer:TelemetryObserverPort):
        self.telemetry_observers.append(observer)

    def start_listening(self):
        self.telemetry_controller.start_listening()

    def stop_listening(self):
        self.telemetry_controller.stop_listening()