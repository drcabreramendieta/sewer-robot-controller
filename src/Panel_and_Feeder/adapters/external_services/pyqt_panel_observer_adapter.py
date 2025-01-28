from Panel_and_Feeder.ports.output import PanelObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData

from Inspection.ports.input import PanelUpdateServicesPort
from PyQt6.QtCore import pyqtSignal, QObject
from logging import Logger

class PyqtPanelObserverAdapter(PanelObserverPort):
    """Adapter to integrate panel observation with PyQt signals.

    Implements observer pattern using PyQt signals for GUI updates
    of robot and camera controls.

    Args:
        panel_update_services (PanelUpdateServicesPort): Service for processing updates
        logger (Logger): Logger instance for operation tracking

    Attributes:
        panel_update_services: Service handling panel updates
        logger: Logger for recording operations
        pyqt_signal_connect: Signal handler instance
    """

    def __init__(self, panel_update_services:PanelUpdateServicesPort, logger:Logger) -> None:
        """Initialize the PyQt panel observer adapter.

        Args:
            panel_update_services (PanelUpdateServicesPort): Update handling service
            logger (Logger): Logger for operation tracking
        """
        super().__init__()
        self.panel_update_services = panel_update_services
        self.logger = logger
        self.pyqt_signal_connect = PyqtSignalConnect(self.panel_update_services)

    def on_robot_control_data_ready(self, robot_control_data:RobotControlData) -> None:
        """Handle new robot control data updates.

        Args:
            robot_control_data (RobotControlData): Updated robot control state

        Raises:
            RuntimeError: If signal emission fails
        """        
        if self.pyqt_signal_connect.robot_control_updated_signal:
            self.pyqt_signal_connect.robot_control_updated_signal.emit(robot_control_data)
    
    def on_camera_control_data_ready(self, camera_control_data:CameraControlData) -> None:
        """Handle new camera control data updates.

        Args:
            camera_control_data (CameraControlData): Updated camera control state

        Raises:
            RuntimeError: If signal emission fails
        """
        if self.pyqt_signal_connect.camera_control_updated_signal:
            self.pyqt_signal_connect.camera_control_updated_signal.emit(camera_control_data)

class PyqtSignalConnect(QObject):
    """PyQt signal handler for panel control updates.

    Manages signal/slot connections for robot and camera control updates.

    Args:
        panel_update_services (PanelUpdateServicesPort): Service receiving updates

    Attributes:
        robot_control_updated_signal (pyqtSignal): Signal for robot updates
        camera_control_updated_signal (pyqtSignal): Signal for camera updates
        panel_update_services: Service handling updates
    """

    robot_control_updated_signal = pyqtSignal(RobotControlData)
    camera_control_updated_signal = pyqtSignal(CameraControlData)
    def __init__(self, panel_update_services:PanelUpdateServicesPort) -> None:
        """Initialize signal connections.

        Args:
            panel_update_services (PanelUpdateServicesPort): Update handling service
        """
        super().__init__()
        self.panel_update_services = panel_update_services
        self.robot_control_updated_signal.connect(self.panel_update_services.update_robot_control)
        self.camera_control_updated_signal.connect(self.panel_update_services.update_camera_control)