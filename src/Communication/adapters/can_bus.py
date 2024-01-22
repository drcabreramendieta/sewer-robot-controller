from Communication.ports.link import RobotLink
from Communication.domain.entities import WheelsModule

class CANRobotLink(RobotLink):
    def send(self, wheelsModule:WheelsModule, speed:int) -> None:
        print(wheelsModule, speed)