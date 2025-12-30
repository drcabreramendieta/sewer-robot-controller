from Inspection.ports.input import FeederUpdateServicePort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
from Inspection.ports.ouput import FeederControllerPort, FeederObserverPort
from typing import List

class FeederUpdateService(FeederUpdateServicePort):
    observers:List[FeederObserverPort]
    def __init__(self, feeder_controller:FeederControllerPort, observer:FeederObserverPort):
        super().__init__()
        self.observers = []
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer)
        self.feeder_controller = feeder_controller

    def register_observer(self, observer:FeederObserverPort):
        self.observers.append(observer)

    def update_feeder_control(self, feeder_control_data:FeederControlData) -> None:
        self._notify(data=feeder_control_data)

    def _notify(self, data: FeederControlData):
        for observer in self.observers:
            observer.on_feeder_ready(data=data)
        
    def send_message(self, msg:str) -> None:
        self.feeder_controller.send_message(msg=msg)
