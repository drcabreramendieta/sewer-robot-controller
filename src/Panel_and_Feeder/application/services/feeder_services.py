from Panel_and_Feeder.ports.input import FeederServicesPort
from Panel_and_Feeder.ports.output.feeder_observer_port import FeederObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
from Panel_and_Feeder.ports.output.panel_and_feeder_controller_port import PanelAndFeederControllerPort
from logging import Logger
from typing import List

class FeederServices(FeederServicesPort):
    observers:List[FeederObserverPort]
    def __init__(self, paf_controller:PanelAndFeederControllerPort, logger:Logger, observer:FeederObserverPort) -> None:
        super().__init__()
        self.observers = []
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer)
        self.paf_controller = paf_controller
        self.logger = logger
        self.paf_controller.feeder_callback_setup(self._notify_feeder_control_data)


    def _notify_feeder_control_data(self, feeder_control_data:FeederControlData) -> None:
        for observer in self.observers:
            observer.on_feeder_control_data_ready(feeder_control_data=feeder_control_data)

    def register_observer(self, observer:FeederObserverPort):
        self.observers.append(observer)

    def start_listening(self):
        print('start')
        self.paf_controller.start_listening()

    def stop_listening(self):
        self.paf_controller.stop_listening()

    def send_message(self, message:str): 
        self.paf_controller.send_message(message)
