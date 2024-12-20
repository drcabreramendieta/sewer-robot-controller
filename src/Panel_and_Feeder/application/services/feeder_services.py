from Panel_and_Feeder.ports.input import FeederServicesPort
from Panel_and_Feeder.ports.output.feeder_observer_port import FeederObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
from Panel_and_Feeder.ports.output.panel_and_feeder_controller_port import PanelAndFeederControllerPort
from logging import Logger

class FeederServices(FeederServicesPort):
    def __init__(self, link:PanelAndFeederControllerPort, logger:Logger) -> None:
        self.feeder_observers:list[FeederObserverPort] = []
        self.link = link
        self.logger = logger
        self.link.feeder_callback_setup(self._notify_feeder_control_data)


    def _notify_feeder_control_data(self, feeder_control_data:FeederControlData) -> None:
        for observer in self.feeder_observers:
            observer.on_feeder_control_data_ready(feeder_control_data=feeder_control_data)

    def register_observer(self, observer:FeederObserverPort):
        self.feeder_observers.append(observer)

    def start_listening(self):
        print('start')
        self.link.start_listening()

    def stop_listening(self):
        self.link.stop_listening()

    def send_message(self, message:str): 
        self.link.send_message(message)