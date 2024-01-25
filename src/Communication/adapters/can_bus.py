from Communication.ports.link import RobotLink
from Communication.domain.entities import WheelsModule, Telemetry, WheelInformation, TelemetryMessage
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
            message1 = can.Message(arbitration_id=0x0202, data=m1, is_extended_id=False)
            message2 = can.Message(arbitration_id=0x0203, data=m2, is_extended_id=False)
            self.bus.send(message1)
            self.bus.send(message2)

        except can.CanError as e:
            print(f"Error CAN: {e}")

    def callback_setup(self, callback:Callable[[Telemetry], None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        self.notifier = can.Notifier(bus=self.bus,listeners=[self._can_message_handler],timeout=2)

    def stop_listening(self) -> None:
        if self.notifier:
            self.notifier.stop(4)
        self.bus.shutdown()

    def _can_message_handler(self,message:can.Message):
        telemetry_message = self._processing_message(message)
        self.callback(telemetry_message)


    def _get_message_type(self, id:int) -> str:
        id_hex = hex(id).split(sep='x')[1]

        if id_hex[0] == '2':
            return 'motor telemetry'
        elif id_hex[0] == '4':
            return 'ECU telemetry'

    def _processing_message(self, message: can.Message) -> TelemetryMessage:
        message_type = self._get_message_type(message.arbitration_id)
        variables = {}
        if message_type == 'motor telemetry':
            if len(message.data) == 8:
                variables['revolution_counter'] = int.from_bytes(message.data[0:2], byteorder='big')
                variables['angular_position'] = int.from_bytes(message.data[2:4], byteorder='big') * 360 / 65535
                variables['speed'] = int.from_bytes(message.data[4:6], byteorder='big')
                variables['current'] = int.from_bytes(message.data[6:8], byteorder='big')

            if len(message.data) == 3:
                variables['voltage'] = int.from_bytes(message.data[0:1], byteorder='big')
                variables['temperature'] = int.from_bytes(message.data[1:2], byteorder='big')
                variables['controller status'] = int(bin(int.from_bytes(message.data[2:3], byteorder='big'))[2])
                variables['calibration status'] = int(bin(int.from_bytes(message.data[2:3], byteorder='big'))[3])
                variables['lock status'] = int(bin(int.from_bytes(message.data[2:3], byteorder='big'))[4])
                variables['voltage control status'] = int(bin(int.from_bytes(message.data[2:3], byteorder='big'))[5:7])
                variables['failure status'] = int(bin(int.from_bytes(message.data[2:3], byteorder='big'))[7:10])
        return TelemetryMessage(message_type=message_type, variables=variables, timestamp=message.timestamp)






        #self.callback(Telemetry(20,20,w_list))
