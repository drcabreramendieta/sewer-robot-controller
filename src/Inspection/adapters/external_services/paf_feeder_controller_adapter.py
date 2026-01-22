from Inspection.ports.output import FeederControllerPort
from Panel_and_Feeder.ports.input import FeederServicesPort

class PafFeederControllerAdapter(FeederControllerPort):
    def __init__(self, feeder_services:FeederServicesPort):
        super().__init__()
        self.feeder_services = feeder_services

    def send_message(self, msg:str) -> None:
        self.feeder_services.send_message(message=msg)