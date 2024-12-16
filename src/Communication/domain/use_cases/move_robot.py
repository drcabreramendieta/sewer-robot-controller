from Communication.ports.output.link import RobotLink
from Communication.domain.entities.entities import WheelsModule
from logging import Logger

class MoveRobot:
    def __init__(self, link:RobotLink, logger:Logger) -> None:
        self.link = link
        self.logger = logger
        

    def run(self, movement:str, speed:int):
        if movement == 'F':
            wheels_module = WheelsModule('F', 'N', speed)
        elif movement == 'B':
            wheels_module = WheelsModule('B', 'N', speed)
        elif movement == 'LF':
            wheels_module = WheelsModule('F', 'L', speed)
        elif movement == 'RF':
            wheels_module = WheelsModule('F', 'R', speed)
        elif movement == 'LB':
            wheels_module = WheelsModule('B', 'L', speed)
        elif movement == 'RB':
            wheels_module = WheelsModule('B', 'R', speed)
        elif movement == 'S':
            wheels_module = WheelsModule('S', 'N', speed)

        self.link.send(wheels_module)
        
