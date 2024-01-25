from Inspection.ports.camera_controller import CameraController
from Communication.domain.use_cases.control_camera import ControlCamera

class GidtecCameraController(CameraController):
    def __init__(self, control_camera:ControlCamera) -> None:
        super().__init__()
        self.control_camera = control_camera

    def tilt_up(self) -> None:
        self.control_camera.run('T', 'U')

    def tilt_down(self) -> None:
        self.control_camera.run('T', 'D')

    def pan_left(self) -> None:
        self.control_camera.run('P', 'L')

    def pan_right(self) -> None:
        self.control_camera.run('P', 'R')

    def focus_in(self) -> None:
        self.control_camera.run('F', 'I')

    def focus_out(self) -> None:
        self.control_camera.run('F', 'O')