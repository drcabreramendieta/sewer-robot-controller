from Panel_and_Feeder.ports.output.panel_and_feeder_controller_port import PanelAndFeederControllerPort
from typing import Callable
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData, FeederControlData, SerialConfig
import threading
import serial
from logging import Logger
from PyQt6.QtCore import QMetaObject, Qt
from PyQt6.QtWidgets import QMessageBox

class SerialPanelAndFeederControllerAdapter(PanelAndFeederControllerPort):
    """Adapter for serial communication with panel and feeder hardware.

    Implements hardware control interface using serial communication.
    Manages data reception through a background thread.

    Args:
        serial_conf (SerialConfig): Serial port configuration
        logger (Logger): Logger for operation tracking

    Attributes:
        robot_callback: Callback for robot control updates
        camera_callback: Callback for camera control updates
        feeder_callback: Callback for feeder control updates
        running: Thread control flag
        thread_capture: Background thread for data capture
    """

    _error_dialog_instance = None
    
    def __init__(self, serial_conf: SerialConfig, logger: Logger) -> None:
        """Initialize serial controller adapter.

        Args:
            serial_conf (SerialConfig): Serial configuration parameters
            logger (Logger): Logger instance
        """
        super().__init__()
        self.robot_callback = None
        self.camera_callback = None
        self.feeder_callback = None
        self.serial_conf = serial_conf
        self.running = None
        self.logger = logger
        self.thread_capture = threading.Thread(target=self._capture_peripheral_data)

    def robot_callback_setup(self, robot_callback: Callable[[RobotControlData], None]) -> None:
        """Set callback for robot control updates.

        Args:
            robot_callback (Callable): Function to handle robot updates
        """
        self.robot_callback = robot_callback

    def camera_callback_setup(self, camera_callback: Callable[[CameraControlData], None]) -> None:
        """Set callback for camera control updates.

        Args:
            camera_callback (Callable): Function to handle camera updates
        """
        self.camera_callback = camera_callback

    def feeder_callback_setup(self, feeder_callback: Callable[[FeederControlData], None]) -> None:
        """Set callback for feeder control updates.

        Args:
            feeder_callback (Callable): Function to handle feeder updates
        """
        self.feeder_callback = feeder_callback

    def start_listening(self) -> None:
        """Start background thread for serial data capture.

        Raises:
            RuntimeError: If thread fails to start
        """
        if not self.running:
            self.running = True
            self.thread_capture.start()
        
    def stop_listening(self) -> None:
        """Stop serial data capture thread.

        Raises:
            RuntimeError: If thread fails to stop
        """
        if self.running:
            self.running = False
            self.thread_capture.join()

    def _process_data(self, data: str) -> None:
        """Process received serial data.

        Args:
            data (str): Raw serial data string

        Raises:
            ValueError: If data format is invalid
        """
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
        """Capture data from serial port in background thread.

        Handles both real serial port and simulated input modes.
        """
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
        """Send message through serial port.

        Args:
            message (str): Message to send

        Raises:
            serial.SerialException: If serial communication fails
        """
        try:
            with serial.Serial(port=self.serial_conf.port, baudrate=self.serial_conf.baudrate, timeout=self.serial_conf.timeout) as ser:
                ser.write((message + "\n").encode())
                print("Mensaje enviado:", message)
        except serial.SerialException as e:
            self.logger.error(f"Error al enviar mensaje: {e}")
            

