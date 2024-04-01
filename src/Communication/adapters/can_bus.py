from Communication.ports.link import RobotLink
from Communication.domain.entities import WheelsModule, TelemetryMessage, CameraStateModule
from typing import Callable
import can
from multipledispatch import dispatch


class CANRobotLink(RobotLink):
    def __init__(self, bus: can.BusABC) -> None:
        self.callback = None
        self.notifier = None
        self.bus = bus

    @dispatch(WheelsModule)
    def send(self, wheelsModule: WheelsModule) -> None:
        # Get the speed message to the wheels modules considering the side. There are two ranges of values 
        # depending on the direction of rotation. The speed values go from -2048 to 2047, with 0 being the change
        # side of rotation.

        if wheelsModule.direction == "F":
            if wheelsModule.rotation == "N":
                m1 = [1, 0, wheelsModule.speed]
            if wheelsModule.rotation == "L":
                m1 = [1, 1, wheelsModule.speed]
            if wheelsModule.rotation == "R":
                m1 = [1, 2, wheelsModule.speed]
        elif wheelsModule.direction == "B":
            if wheelsModule.rotation == "N":
                m1 = [2, 0, wheelsModule.speed]
            if wheelsModule.rotation == "L":
                m1 = [2, 1, wheelsModule.speed]
            if wheelsModule.rotation == "R":
                m1 = [2, 2, wheelsModule.speed]
        elif wheelsModule.direction == "S":
            m1 = [0, 0, wheelsModule.speed]

        print(m1)
        # Configure CAN protocol communication
        try:
            message1 = can.Message(arbitration_id=0x0001, data=m1, is_extended_id=False)
            self.bus.send(message1)
        except can.CanError as e:
            print(f"Error CAN: {e}")

    # TODO: Implement specific behaviors
    def initialize_camera(self, camera_state: CameraStateModule) -> bool:
        m1 = [0x77, 0x74]
        print(m1)
        # Configure CAN protocol communication
        try:
            message1 = can.Message(arbitration_id=0x0002, data=m1, is_extended_id=False)
            self.bus.send(message1)
            print(message1)
        except can.CanError as e:
            print(f"Error CAN: {e}")
        return True

    @dispatch(CameraStateModule)
    def send(self, module: CameraStateModule) -> None:
        if (module.focus == "O"):
            byte1 = 0x94
        elif (module.focus == "I"):
            byte1 = 0x91
        elif (module.focus == "S"):
            byte1 = 0x04

        if (module.pan == "R"):
            byte2 = 0x44
        elif (module.pan == "L"):
            byte2 = 0x33
        elif (module.pan == "S"):
            byte2 = 0x02

        if (module.tilt == "U"):
            byte3 = 0x11
        elif (module.tilt == "D"):
            byte3 = 0x22
        elif (module.tilt == "S"):
            byte3 = 0x01

        if (0 <= module.light < 11):
            byte4 = 0x2a
        elif (11 <= module.light < 22):
            byte4 = 0x3a
        elif (22 <= module.light < 33):
            byte4 = 0x4a
        elif (33 <= module.light < 44):
            byte4 = 0x5a
        elif (44 <= module.light < 55):
            byte4 = 0x6a
        elif (55 <= module.light < 66):
            byte4 = 0x9a
        elif (66 <= module.light < 77):
            byte4 = 0x5b
        elif (77 <= module.light < 88):
            byte4 = 0x9b
        elif (88 <= module.light <= 100):
            byte4 = 0x6c

        m1 = [byte1, byte2, byte3, byte4]

        print(m1)
        # Configure CAN protocol communication
        try:
            message1 = can.Message(arbitration_id=0x0003, data=m1, is_extended_id=False)
            self.bus.send(message1)
            print(message1)
        except can.CanError as e:
            print(f"Error CAN: {e}")

    def callback_setup(self, callback: Callable[[TelemetryMessage], None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        self.notifier = can.Notifier(bus=self.bus, listeners=[self._can_message_handler], timeout=2)

    def stop_listening(self) -> None:
        if self.notifier:
            self.notifier.stop(4)
        self.bus.shutdown()

    def _can_message_handler(self, message: can.Message):
        telemetry_message = self._processing_message(message)
        self.callback(telemetry_message)

    def _get_message_type(self, id: int) -> str:
        id_hex = hex(id).split(sep='x')[1]

        if (id_hex[0] == '2' and id_hex[1] == '0' and id_hex[2] == '8'):
            return 'motor telemetry'
        elif (id_hex[0] == '4' and id_hex[1] == '0' and id_hex[2] == '0'):
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
        
        if message_type == 'ECU telemetry':
            if len(message.data) == 8:
                variables['Temperature'] = int.from_bytes(message.data[0:1], byteorder='big')
                variables['Humidity'] = int.from_bytes(message.data[1:2], byteorder='big') 
                variables['X slop'] = int.from_bytes(message.data[2:4], byteorder='big')
                variables['Y slop'] = int.from_bytes(message.data[4:6], byteorder='big')

        return TelemetryMessage(message_type=message_type, variables=variables, timestamp=message.timestamp) 
        # self.callback(Telemetry(20,20,w_list))
