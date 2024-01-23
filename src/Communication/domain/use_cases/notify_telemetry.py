from Communication.ports.observer import TelemetryObserver
from Communication.domain.entities import Telemetry
from Communication.ports.link import RobotLink

class NotifyTelemetry:
    def __init__(self, telemetry_observers:list[TelemetryObserver], link:RobotLink) -> None:
        self.telemetry_observers = telemetry_observers
        self.link = link
        link.callback_setup(self._notify)

    def _notify(self, telemetry:Telemetry) -> None:
        for observer in self.telemetry_observers:
            observer.on_telemetry_ready(telemetry=telemetry)

    def start_listening(self):
        self.link.start_listening()

    def stop_listening(self):
        self.link.stop_listening()