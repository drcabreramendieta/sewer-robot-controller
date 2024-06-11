from Inspection.ports.robot_controller import RobotController
from Communication.domain.use_cases.move_robot import MoveRobot
from logging import Logger

class GidtecRobotController(RobotController):
    def __init__(self, communication_controller:MoveRobot, logger:Logger) -> None:
        super().__init__()
        self.communication_controller = communication_controller
        self.logger = logger
        self.value = 3
        
    def change_speed(self, value:int) -> None:
        self.value = value  

    def move_forward(self) -> None:
        self.communication_controller.run('F', self.value)

    def move_backward(self) -> None:
        self.communication_controller.run('B', self.value)

    def rotate_left_forward(self) -> None:
        self.communication_controller.run('LF', self.value)

    def rotate_right_forward(self) -> None:
        self.communication_controller.run('RF', self.value)

    def rotate_left_backward(self) -> None:
        self.communication_controller.run('LB', self.value)

    def rotate_right_backward(self) -> None:
        self.communication_controller.run('RB', self.value)
        
    def stop(self) -> None:
        self.communication_controller.run('S', 0)