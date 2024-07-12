from Panel_and_Feeder.ports.peripheral_link import PeripheralLink
from typing import Callable
from Panel_and_Feeder.domain.entities import RobotControlData, CameraControlData, FeederControlData, SerialConfig
import threading
import serial
from logging import Logger
from PyQt6.QtCore import QMetaObject, Qt
from PyQt6.QtWidgets import QMessageBox

class SerialPeripheralLink(PeripheralLink):
    _error_dialog_instance = None
    
    def __init__(self, serial_conf: SerialConfig, logger: Logger) -> None:
        super().__init__()
        self.robot_callback = None
        self.camera_callback = None
        self.feeder_callback = None
        self.serial_conf = serial_conf
        self.running = None
        self.logger = logger
        self.thread_capture = threading.Thread(target=self._capture_peripheral_data)

    def robot_callback_setup(self, robot_callback: Callable[[RobotControlData], None]) -> None:
        self.robot_callback = robot_callback

    def camera_callback_setup(self, camera_callback: Callable[[CameraControlData], None]) -> None:
        self.camera_callback = camera_callback

    def feeder_callback_setup(self, feeder_callback: Callable[[FeederControlData], None]) -> None:
        self.feeder_callback = feeder_callback

    def start_listening(self) -> None:
        if not self.running:
            self.running = True
            self.thread_capture.start()
        
    def stop_listening(self) -> None:
        if self.running:
            self.running = False
            self.thread_capture.join()

    def _process_data(self, data: str) -> None:
        print('Arrived data:', data)
        data = data.decode('utf-8').strip()
        data_fields = data.split(sep=' ')
        if data_fields[0] == 'robot':
            direction = data_fields[1]
            robot_control_data = RobotControlData(direction=direction)
            self.robot_callback(robot_control_data)
        elif data_fields[0] == 'camera':
            movement = data_fields[1]
            light = data_fields[2]
            camera_control_data = CameraControlData(movement=movement, light=light)
            self.camera_callback(camera_control_data)
        elif data_fields[0] == 'feeder':
            distance = data_fields[1]
            reset = data_fields[2]
            feeder_control_data = FeederControlData(distance=distance, reset=reset)
            self.feeder_callback(feeder_control_data)

    def _capture_peripheral_data(self):
        if self.serial_conf.port == '':
            while self.running:
                data = input("Ingresa datos seriales:")
                self._process_data(data=data)
        else:
            try:
                with serial.Serial(port=self.serial_conf.port, baudrate=self.serial_conf.baudrate, timeout=self.serial_conf.timeout) as ser:
                    while self.running:
                        data = ser.readline()
                        if data:
                            self._process_data(data=data)
            except serial.SerialException as e:
                self.logger.error(f"Error opening or reading from serial port: {e}")
                              
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                
            finally:
                if 'ser' in locals() and ser.is_open:
                    ser.close()
                print("Finalizando el hilo de captura de datos serial.")

    def send_message(self, message: str):
        try:
            with serial.Serial(port=self.serial_conf.port, baudrate=self.serial_conf.baudrate, timeout=self.serial_conf.timeout) as ser:
                ser.write((message + "\n").encode())
                print("Mensaje enviado:", message)
        except serial.SerialException as e:
            self.logger.error(f"Error al enviar mensaje: {e}")
            

