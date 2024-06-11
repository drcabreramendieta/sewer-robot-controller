from Communication.ports.observer import TelemetryObserver
from Communication.domain.entities import TelemetryMessage
from Communication.ports.link import RobotLink
from logging import Logger

class NotifyTelemetry:
    def __init__(self, link:RobotLink, logger:Logger, telemetry_observers:list[TelemetryObserver]|None=None) -> None:
        self.telemetry_observers = telemetry_observers if telemetry_observers else [] 
        self.link = link
        self.logger = logger
        link.callback_setup(self._notify)

    def _notify(self, telemetry:TelemetryMessage) -> None:
        for observer in self.telemetry_observers:
            observer.on_telemetry_ready(telemetry=telemetry)

    def register_observer(self, observer:TelemetryObserver):
        self.telemetry_observers.append(observer)

    def start_listening(self):
        self.link.start_listening()

    def stop_listening(self):
        self.link.stop_listening()