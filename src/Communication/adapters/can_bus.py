from Communication.ports.link import RobotLink
from Communication.domain.entities import WheelsModule, Telemetry, WheelInformation
from typing import Callable
import can

class CANRobotLink(RobotLink):
    def __init__(self, bus:can.Bus) -> None:
        self.callback = None
        self.notifier = None
        self.bus = bus

    def send(self, wheelsModuleLeft:WheelsModule, wheelsModuleRight:WheelsModule) -> None:
        # Get the speed message to the wheels modules considering the side. There are two ranges of values 
        # depending on the direction of rotation. The speed values go from -2048 to 2047, with 0 being the change
        # side of rotation.
        speed_left = 0
        speed_right = 0

        if wheelsModuleLeft.direction == "F":
            speed_left = int(-2048 * (wheelsModuleLeft.speed / 100))
        elif wheelsModuleLeft.direction == "B":
            speed_left = int(2047 * (wheelsModuleLeft.speed / 100))
        elif wheelsModuleLeft.direction == "S":
            speed_left = 0

        if wheelsModuleRight.direction == "F":
            speed_right = int(2047 * (wheelsModuleRight.speed / 100))
        elif wheelsModuleRight.direction == "B":
            speed_right = int(-2048 * (wheelsModuleRight.speed / 100))
        elif wheelsModuleRight.direction == "S":
            speed_right = 0

        speed_left = format((speed_left + (1 << 16)) % (1 << 16), '0{}b'.format(16))
        speed_left_data0 = int(speed_left[:8], 2)
        speed_left_data1 = int(speed_left[8:], 2)

        speed_right = format((speed_right + (1 << 16)) % (1 << 16), '0{}b'.format(16))
        speed_right_data0 = int(speed_right[:8], 2)
        speed_right_data1 = int(speed_right[8:], 2)

        m1 = [speed_left_data0, speed_left_data1, speed_left_data0, speed_left_data1, speed_left_data0,
              speed_left_data1, speed_right_data0, speed_right_data1]
        m2 = [speed_right_data0, speed_right_data1, speed_right_data0, speed_right_data1, 0, 0, 0, 0]

        print(m1)
        # Configure CAN protocol communication
        try:
            bus = can.interface.Bus(device_id=0, interface='pcan', bitrate=1000000)
            message1 = can.Message(arbitration_id=0x0202, data=m1, is_extended_id=False)
            message2 = can.Message(arbitration_id=0x0203, data=m2, is_extended_id=False)
            print(message1)
            print(message2)
            bus.send(message1)
            bus.send(message2)

            print('Mensaje enviado')

        except can.CanError as e:
            print(f"Error CAN: {e}")

        finally:
            if 'bus' in locals():
                bus.shutdown()
    
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
