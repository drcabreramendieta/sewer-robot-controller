from Panel_and_Feeder.ports.feeder_observer import FeederObserver
from Panel_and_Feeder.domain.entities import FeederControlData
from PyQt6.QtCore import pyqtSignal
from logging import Logger

class QtFeederObserver(FeederObserver):
    feeder_control_changed_signal = pyqtSignal(FeederControlData)
    def __init__(self, logger:Logger) -> None:
        super().__init__()
        self.feeder_control_changed_signal = None
        self.logger = logger

    def on_feeder_control_data_ready(self, feeder_control_data:FeederControlData) -> None:
        if self.feeder_control_changed_signal:
            self.feeder_control_changed_signal.emit(feeder_control_data)

    def register_feeder_signal(self, signal:pyqtSignal):
        self.feeder_control_changed_signal = signal