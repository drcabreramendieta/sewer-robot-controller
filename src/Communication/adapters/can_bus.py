from Communication.ports.output.link import RobotLink
from Communication.domain.entities.entities import WheelsModule, TelemetryMessage, CameraStateModule
from typing import Callable
import can
from multipledispatch import dispatch
from logging import Logger
from Inspection.ui.main_window import MainWindow


class CANError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

class CANRobotLink(RobotLink):
    def __init__(self, bus: can.BusABC, logger: Logger) -> None:
        self.callback = None
        self.notifier = None
        self.bus = bus
        self.logger = logger

    @dispatch(WheelsModule)
    def send(self, wheelsModule: WheelsModule) -> None:
        if wheelsModule.direction == "F":
            if wheelsModule.rotation == "N":
                m1 = [1, 0, wheelsModule.speed]
            elif wheelsModule.rotation == "L":
                m1 = [1, 1, wheelsModule.speed]
            elif wheelsModule.rotation == "R":
                m1 = [1, 2, wheelsModule.speed]
        elif wheelsModule.direction == "B":
            if wheelsModule.rotation == "N":
                m1 = [2, 0, wheelsModule.speed]
            elif wheelsModule.rotation == "L":
                m1 = [2, 1, wheelsModule.speed]
            elif wheelsModule.rotation == "R":
                m1 = [2, 2, wheelsModule.speed]
        elif wheelsModule.direction == "S":
            m1 = [0, 0, wheelsModule.speed]

        #self.logger.info(f"Sending wheels module message: {m1}")
        try:
            message1 = can.Message(arbitration_id=0x0001, data=m1, is_extended_id=False)
            self.bus.send(message1)
            self.logger.info("Robot message sent successfully")
        except can.CanError as e:
            self.logger.error(f"CAN Error: {e}")
            if e.error_code == 100:  # Network is down
                self.logger.error("Network is down")
                MainWindow.show_error_dialog_restart()
            elif e.error_code == 6:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()
            else:
                self.logger.error("Unknown CAN error")
                MainWindow.show_error_dialog_restart()
        except OSError as e:
            self.logger.error(f"OSError: {e}")
            if e.errno == 19:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()

    def initialize_camera(self, camera_state: CameraStateModule) -> bool:
        m1 = [0x77, 0x74]
        #self.logger.info(f"Initializing camera with message: {m1}")
        try:
            message1 = can.Message(arbitration_id=0x0002, data=m1, is_extended_id=False)
            self.bus.send(message1)
            self.logger.info("Camera initialization message sent successfully")
        except can.CanError as e:
            self.logger.error(f"CAN Error: {e}")
            if e.error_code == 100:  # Network is down
                self.logger.error("Network is down")
                MainWindow.show_error_dialog_restart()
            elif e.error_code == 6:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()
            else:
                self.logger.error("Unknown CAN error")
                MainWindow.show_error_dialog_restart()
        except OSError as e:
            self.logger.error(f"OSError: {e}")
            if e.errno == 19:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()
        return True

    @dispatch(CameraStateModule)
    def send(self, module: CameraStateModule) -> None:
        if module.focus == "O":
            byte1 = 0x94
        elif module.focus == "I":
            byte1 = 0x91
        elif module.focus == "S":
            byte1 = 0x04

        if module.pan == "R":
            byte2 = 0x44
        elif module.pan == "L":
            byte2 = 0x33
        elif module.pan == "S":
            byte2 = 0x02

        if module.tilt == "U":
            byte3 = 0x11
        elif module.tilt == "D":
            byte3 = 0x22
        elif module.tilt == "S":
            byte3 = 0x01

        if 0 <= module.light < 11:
            byte4 = 0x2a
        elif 11 <= module.light < 22:
            byte4 = 0x3a
        elif 22 <= module.light < 33:
            byte4 = 0x4a
        elif 33 <= module.light < 44:
            byte4 = 0x5a
        elif 44 <= module.light < 55:
            byte4 = 0x6a
        elif 55 <= module.light < 66:
            byte4 = 0x9a
        elif 66 <= module.light < 77:
            byte4 = 0x5b
        elif 77 <= module.light < 88:
            byte4 = 0x9b
        elif 88 <= module.light <= 100:
            byte4 = 0x6c

        m1 = [byte1, byte2, byte3, byte4]

        #self.logger.info(f"Sending camera state module message: {m1}")
        try:
            message1 = can.Message(arbitration_id=0x0003, data=m1, is_extended_id=False)
            self.bus.send(message1)
            self.logger.info("Camera message sent successfully")
        except can.CanError as e:
            self.logger.error(f"CAN Error: {e}")
            if e.error_code == 100:  # Network is down
                self.logger.error("Network is down")
                MainWindow.show_error_dialog_restart()
            elif e.error_code == 6:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()
            else:
                self.logger.error("Unknown CAN error")
                MainWindow.show_error_dialog_restart()
        except OSError as e:
            self.logger.error(f"OSError: {e}")
            if e.errno == 19:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()

    def callback_setup(self, callback: Callable[[TelemetryMessage], None]) -> None:
        self.callback = callback
        #self.logger.info("Callback setup completed")

    def start_listening(self) -> None:
        try:
            self.notifier = can.Notifier(bus=self.bus, listeners=[self._can_message_handler], timeout=2)
            #self.logger.info("Started listening for CAN messages")
        except can.CanError as e:
            self.logger.error(f"Error CAN: {e}")
            if e.error_code == 100:  # Network is down
                self.logger.error("Network is down")
                MainWindow.show_error_dialog_restart()
            elif e.error_code == 6:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()
            else:
                self.logger.error("Unknown CAN error")
                MainWindow.show_error_dialog_restart()
        except OSError as e:
            self.logger.error(f"OSError: {e}")
            if e.errno == 19:  # No such device or address
                self.logger.error("No such device or address")
                MainWindow.show_error_dialog_restart()

    def stop_listening(self) -> None:
        if self.notifier:
            self.notifier.stop(4)
            #self.logger.info("Stopped listening for CAN messages")
        self.bus.shutdown()
        self.logger.info("CAN bus shutdown completed")

    def _can_message_handler(self, message: can.Message):
        try:
            telemetry_message = self._processing_message(message)
            self.callback(telemetry_message)
            #self.logger.info("Processed CAN message successfully")
        except Exception as e:
            self.logger.error(f"Error processing CAN message: {e}")

    def _get_message_type(self, id: int) -> str:
        id_hex = hex(id).split(sep='x')[1]

        if id_hex[0] == '2' and id_hex[1] == '0' and id_hex[2] == '8':
            return 'motor telemetry'
        elif id_hex[0] == '4' and id_hex[1] == '0' and id_hex[2] == '0':
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
                variables['Motor status'] = int.from_bytes(message.data[6:7], byteorder='big')

            if int.from_bytes(message.data[6:7], byteorder='big') == 0xC0:
                self.logger.info("No warnings.")
            elif int.from_bytes(message.data[6:7], byteorder='big') == 0xE0:
                self.logger.info(self.tr("Caution locked wheels."))

        return TelemetryMessage(message_type=message_type, variables=variables, timestamp=message.timestamp)
