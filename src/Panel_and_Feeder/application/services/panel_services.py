from Panel_and_Feeder.ports.input import PanelServicesPort
from Panel_and_Feeder.ports.output.panel_observer_port import PanelObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData
from Panel_and_Feeder.ports.output.panel_and_feeder_controller_port import PanelAndFeederControllerPort
from logging import Logger
from typing import List

class PanelServices(PanelServicesPort):
    observers:List[PanelObserverPort]
    def __init__(self, paf_controller:PanelAndFeederControllerPort, logger:Logger) -> None:
        super().__init__()
        self.observers = []
        self.paf_controller = paf_controller
        self.logger = logger
        self.paf_controller.robot_callback_setup(self._notify_robot_control_data)
        self.paf_controller.camera_callback_setup(self._notify_camera_control_data)

    def _notify_robot_control_data(self, robot_control_data:RobotControlData) -> None:
        for observer in self.observers:
            observer.on_robot_control_data_ready(robot_control_data=robot_control_data)

    def _notify_camera_control_data(self, camera_control_data:CameraControlData) -> None:
        for observer in self.observers:
            observer.on_camera_control_data_ready(camera_control_data=camera_control_data)

    def register_observer(self, observer:PanelObserverPort):
        self.observers.append(observer)

    def start_listening(self):
        print('start')
        self.paf_controller.start_listening()

    def stop_listening(self):
        self.paf_controller.stop_listening()
