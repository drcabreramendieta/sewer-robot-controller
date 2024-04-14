from Panel_and_Feeder.ports.panel_observer import PanelObserver
from Panel_and_Feeder.domain.entities import RobotControlData, CameraControlData
from Panel_and_Feeder.ports.peripheral_link import PeripheralLink

class PanelNotifier:
    def __init__(self, link:PeripheralLink) -> None:
        self.panel_observers:list[PanelObserver] = []
        self.link = link
        self.link.robot_callback_setup(self._notify_robot_control_data)
        self.link.camera_callback_setup(self._notify_camera_control_data)

    def _notify_robot_control_data(self, robot_control_data:RobotControlData) -> None:
        for observer in self.panel_observers:
            observer.on_robot_control_data_ready(robot_control_data=robot_control_data)

    def _notify_camera_control_data(self, camera_control_data:CameraControlData) -> None:
        for observer in self.panel_observers:
            observer.on_camera_control_data_ready(camera_control_data=camera_control_data)

    def register_observer(self, observer:PanelObserver):
        self.panel_observers.append(observer)

    def start_listening(self):
        print('start')
        self.link.start_listening()

    def stop_listening(self):
        self.link.stop_listening()