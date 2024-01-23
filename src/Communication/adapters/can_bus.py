from Communication.ports.link import RobotLink
from Communication.domain.entities import WheelsModule, Telemetry, WheelInformation
from typing import Callable
import can

class CANRobotLink(RobotLink):
    def __init__(self, bus:can.Bus) -> None:
        self.callback = None
        self.notifier = None
        self.bus = bus

    def send(self, wheelsModule:WheelsModule) -> None:
        print(wheelsModule)

    def callback_setup(self, callback:Callable[[Telemetry], None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        self.notifier = can.Notifier(bus=self.bus,listeners=[self._can_message_handler],timeout=2)

    def stop_listening(self) -> None:
        self.notifier.bus.shutdown()

    def _can_message_handler(self,message:can.Message):
        print(message)
        w1 = WheelInformation(10,30)
        w2 = WheelInformation(30,40)
        w_list = list()
        w_list.append(w1)
        w_list.append(w2)
        self.callback(Telemetry(20,20,w_list))
