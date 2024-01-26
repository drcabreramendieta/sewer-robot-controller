from Communication.ports.link import RobotLink
from Communication.domain.entities import CameraStateModule

class ControlCamera:
    def __init__(self, robot_link:RobotLink) -> None:
        self.robot_link = robot_link
        self.camera_state = CameraStateModule(initialized=False, tilt='S',pan='S',focus='S',zoom='S',light=0)

    def run(self, module:str, order:str|int|None=None) -> None:        
        if module == 'I':
            self.camera_state.initialized = self.robot_link.initialize_camera(self.camera_state)
        elif module == 'L':
            self.camera_state.light = order
            self.robot_link.send(self.camera_state)
        elif self.camera_state.initialized:
            if module == 'T':
                self.camera_state.tilt = order
            elif module == 'P':
                self.camera_state.pan = order
            elif module == 'F':
                self.camera_state.focus = order
            self.robot_link.send(self.camera_state)