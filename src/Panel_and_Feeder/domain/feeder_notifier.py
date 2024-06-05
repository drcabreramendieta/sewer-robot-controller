from Panel_and_Feeder.ports.feeder_observer import FeederObserver
from Panel_and_Feeder.domain.entities import FeederControlData
from Panel_and_Feeder.ports.peripheral_link import PeripheralLink

class FeederNotifier:
    def __init__(self, link:PeripheralLink) -> None:
        self.feeder_observers:list[FeederObserver] = []
        self.link = link
        self.link.feeder_callback_setup(self._notify_feeder_control_data)


    def _notify_feeder_control_data(self, feeder_control_data:FeederControlData) -> None:
        for observer in self.feeder_observers:
            observer.on_feeder_control_data_ready(feeder_control_data=feeder_control_data)

    def register_observer(self, observer:FeederObserver):
        self.feeder_observers.append(observer)

    def start_listening(self):
        print('start')
        self.link.start_listening()

    def stop_listening(self):
        self.link.stop_listening()

    def send_message(self, message:str): 
        self.link.send_message(message)