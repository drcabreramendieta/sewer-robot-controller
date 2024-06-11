from Communication.ports.observer import TelemetryObserver
from Communication.domain.entities import TelemetryMessage
from PyQt6.QtCore import pyqtSignal
from logging import Logger

class TestTelemetryObserver(TelemetryObserver):
    telemetry_updated_signal = pyqtSignal(TelemetryMessage)
    def __init__(self, logger:Logger) -> None:
        super().__init__()
        self.telemetry_updated_signal = None
        self.logger = logger

    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        if self.telemetry_updated_signal:
            self.telemetry_updated_signal.emit(telemetry)

    def register_signal(self, signal: pyqtSignal): 
        self.telemetry_updated_signal = signal 
