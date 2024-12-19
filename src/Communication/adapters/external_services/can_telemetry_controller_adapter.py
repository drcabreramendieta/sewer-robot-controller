from Communication.ports.output import TelemetryControllerPort
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from typing import Callable
import can
from logging import Logger

class CanTelemetryControllerAdapter(TelemetryControllerPort):
    def __init__(self, bus: can.BusABC, logger: Logger) -> None:
        self.callback = None
        self.notifier = None
        self.bus = bus
        self.logger = logger

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
            elif e.error_code == 6:  # No such device or address
                self.logger.error("No such device or address")
            else:
                self.logger.error("Unknown CAN error")
        except OSError as e:
            self.logger.error(f"OSError: {e}")
            if e.errno == 19:  # No such device or address
                self.logger.error("No such device or address")

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
