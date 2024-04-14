from Panel_and_Feeder.ports.peripheral_link import PeripheralLink
from typing import Callable
from Panel_and_Feeder.domain.entities import RobotControlData, CameraControlData, FeederControlData, SerialConfig
import threading
import serial

class SerialPeripheralLink(PeripheralLink):
    def __init__(self, serial_conf:SerialConfig) -> None:
        super().__init__()
        self.robot_callback = None
        self.camera_callback = None
        self.feeder_callback = None
        self.serial_conf = serial_conf
        self.running = None
        self.thread_capture = threading.Thread(target=self._capture_peripheral_data)

    def robot_callback_setup(self, robot_callback:Callable[[RobotControlData],None]) -> None:
        self.robot_callback = robot_callback

    def camera_callback_setup(self, camera_callback:Callable[[CameraControlData],None]) -> None:
        self.camera_callback = camera_callback

    def feeder_callback_setup(self, feeder_callback:Callable[[FeederControlData],None]) -> None:
        self.feeder_callback = feeder_callback

    def start_listening(self) -> None:
        if not self.running:
            self.running = True
            self.thread_capture.start()
        
    def stop_listening(self) -> None:
        if self.running:
            self.running = False
            self.thread_capture.join()

    def _process_data(self, data:str) -> None:
        print('Arrived data:', data)
        data_fields = data.split(sep=' ')
        if data_fields[0] == 'robot':
            # TODO: Process data for robot and create RobotControlData instance
            robot_control_data = RobotControlData(speed='speed', direction='direction')
            self.robot_callback(robot_control_data)
        elif data_fields[0] == 'camera':
            # TODO: Process data for camera and create CameraControlData instance
            camera_control_data = CameraControlData(pan='pan', tilt='tilt', light='light')
            self.camera_callback(camera_control_data)
        elif data_fields[0] == 'feeder':
            # TODO: Process data for feeder and create FeederControlData instance
            feeder_control_data = FeederControlData(speed='speed', direction='direction')
            self.feeder_callback(feeder_control_data)

    def _capture_peripheral_data(self):
        if self.serial_conf.port == '':
            while self.running:
                data = input("Ingresa datos seriales:")
                self._process_data(data=data)
        else:
            with serial.Serial(port=self.serial_conf.port, baudrate=self.serial_conf.baudrate, timeout=self.serial_conf.timeout) as ser:
                while self.running:
                    data = ser.readline()
                    data = input("Ingresa datos seriales:")
                    self._process_data(data=data)
        