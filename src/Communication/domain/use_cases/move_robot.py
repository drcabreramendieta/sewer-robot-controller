from Communication.ports.link import RobotLink
from Communication.domain.entities import WheelsModule

class MoveRobot:
    def __init__(self, link:RobotLink) -> None:
        self.link = link

    def run(self, movement:str, speed:int):
        if movement == 'F':
            left_wheels = WheelsModule('L', 'F', speed)
            right_wheels = WheelsModule('R', 'F', speed)
        elif movement == 'B':
            left_wheels = WheelsModule('L', 'B', speed)
            right_wheels = WheelsModule('R', 'B', speed)
        elif movement == 'L':
            left_wheels = WheelsModule('L', 'B', speed)
            right_wheels = WheelsModule('R', 'F', speed)
        elif movement == 'R':
            left_wheels = WheelsModule('L', 'F', speed)
            right_wheels = WheelsModule('R', 'B', speed)    
        elif movement == 'S':
            left_wheels = WheelsModule('L', 'S', speed)
            right_wheels = WheelsModule('R', 'S', speed)

        self.link.send(left_wheels)
        self.link.send(right_wheels)
