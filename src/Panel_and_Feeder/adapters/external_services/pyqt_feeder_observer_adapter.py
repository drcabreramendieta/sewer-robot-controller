from Panel_and_Feeder.ports.output import FeederObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData

from Inspection.ports.input import FeederUpdateServicePort
from PyQt6.QtCore import pyqtSignal, QObject
from logging import Logger

class PyqtFeederObserverAdapter(FeederObserverPort):
    def __init__(self, feeder_update_service:FeederUpdateServicePort, logger:Logger) -> None:
        super().__init__()
        self.feeder_update_service = feeder_update_service
        self.logger = logger
        self.pyqt_signal_connect = PyqtSignalConnect(self.feeder_update_service)

    def on_feeder_control_data_ready(self, feeder_control_data:FeederControlData) -> None:
        if self.pyqt_signal_connect.feeder_control_updated_signal:
            self.pyqt_signal_connect.feeder_control_updated_signal.emit(feeder_control_data)
    

class PyqtSignalConnect(QObject):
    feeder_control_updated_signal = pyqtSignal(FeederControlData)
    def __init__(self, feeder_update_service:FeederUpdateServicePort) -> None:
        super().__init__()
        self.feeder_update_service = feeder_update_service
        self.feeder_control_updated_signal.connect(self.feeder_update_service.update_feeder_control)