from Communication.ports.link import RobotLink
from Communication.domain.entities import TiltModule, PanModule, FocusModule

class ControlCamera:
    def __init__(self, robot_link:RobotLink) -> None:
        self.robot_link = robot_link

    def run(self, module:str, direction:str):
        if module == 'T':
            self.robot_link.send(TiltModule(direction))
        elif module == 'P':
            self.robot_link.send(PanModule(direction))
        elif module == 'F':
            self.robot_link.send(FocusModule(direction))