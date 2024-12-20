from Panel_and_Feeder.ports.input import PanelServicesPort
from Panel_and_Feeder.ports.output.panel_observer_port import PanelObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData
from Panel_and_Feeder.ports.output.panel_and_feeder_controller_port import PanelAndFeederControllerPort
from logging import Logger

class PanelServices(PanelServicesPort):
    def __init__(self, link:PanelAndFeederControllerPort, logger:Logger) -> None:
        self.panel_observers:list[PanelObserverPort] = []
        self.link = link
        self.logger = logger
        self.link.robot_callback_setup(self._notify_robot_control_data)
        self.link.camera_callback_setup(self._notify_camera_control_data)

    def _notify_robot_control_data(self, robot_control_data:RobotControlData) -> None:
        for observer in self.panel_observers:
            observer.on_robot_control_data_ready(robot_control_data=robot_control_data)

    def _notify_camera_control_data(self, camera_control_data:CameraControlData) -> None:
        for observer in self.panel_observers:
            observer.on_camera_control_data_ready(camera_control_data=camera_control_data)

    def register_observer(self, observer:PanelObserverPort):
        self.panel_observers.append(observer)

    def start_listening(self):
        print('start')
        self.link.start_listening()

    def stop_listening(self):
        self.link.stop_listening()