from Inspection.ports.robot_controller import RobotController
from Communication.domain.use_cases.move_robot import MoveRobot

class GidtecRobotController(RobotController):
    def __init__(self, communication_controller:MoveRobot) -> None:
        super().__init__()
        self.communication_controller = communication_controller

    def move_forward(self) -> None:
        self.communication_controller.run('F', 10)

    def move_backward(self) -> None:
        self.communication_controller.run('B', 10)

    def rotate_left_forward(self) -> None:
        self.communication_controller.run('LF', 10)

    def rotate_right_forward(self) -> None:
        self.communication_controller.run('RF', 10)

    def rotate_left_backward(self) -> None:
        self.communication_controller.run('LB', 10)

    def rotate_right_backward(self) -> None:
        self.communication_controller.run('RB', 10)
        
    def stop(self) -> None:
        self.communication_controller.run('S', 0)