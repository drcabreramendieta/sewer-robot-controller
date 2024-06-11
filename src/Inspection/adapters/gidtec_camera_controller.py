from Inspection.ports.camera_controller import CameraController
from Communication.domain.use_cases.control_camera import ControlCamera
from logging import Logger

class GidtecCameraController(CameraController):
    def __init__(self, control_camera:ControlCamera, logger:Logger) -> None:
        super().__init__()
        self.control_camera = control_camera
        self.logger = logger

    def tilt_up(self) -> None:
        self.control_camera.run('T', 'U')

    def tilt_down(self) -> None:
        self.control_camera.run('T', 'D')

    def tilt_stop(self) -> None:
        self.control_camera.run('T', 'S')

    def pan_left(self) -> None:
        self.control_camera.run('P', 'L')

    def pan_right(self) -> None:
        self.control_camera.run('P', 'R')

    def pan_stop(self) -> None:
        self.control_camera.run('P', 'S')

    def focus_in(self) -> None:
        self.control_camera.run('F', 'I')

    def focus_out(self) -> None:
        self.control_camera.run('F', 'O')

    def focus_stop(self) -> None:
        self.control_camera.run('F', 'S')

    def change_light(self, value:int) -> None:
        self.control_camera.run('L', value)

    def init_camera(self) -> None:
        self.control_camera.run('I')