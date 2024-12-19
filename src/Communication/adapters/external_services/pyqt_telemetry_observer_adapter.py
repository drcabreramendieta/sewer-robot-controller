from Communication.ports.output import TelemetryObserverPort
from Communication.domain.entities.telemetry_entities import TelemetryMessage

from Inspection.ports.input import TelemetryUpdateServicePort
from PyQt6.QtCore import pyqtSignal, QObject
from logging import Logger

class PyqtTelemetryObserverAdapter(TelemetryObserverPort):
    def __init__(self, telemetry_update_service:TelemetryUpdateServicePort, logger:Logger) -> None:
        super().__init__()
        self.telemetry_update_service = telemetry_update_service
        self.logger = logger
        self.pyqt_signal_connect = PyqtSignalConnect(self.telemetry_update_service)

    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        if self.pyqt_signal_connect.telemetry_updated_signal:
            self.pyqt_signal_connect.telemetry_updated_signal.emit(telemetry)

class PyqtSignalConnect(QObject):
    telemetry_updated_signal = pyqtSignal(TelemetryMessage)
    def __init__(self, telemetry_update_service:TelemetryUpdateServicePort) -> None:
        super().__init__()
        self.telemetry_update_service = telemetry_update_service
        self.telemetry_updated_signal.connect(self.telemetry_update_service.update_telemetry)