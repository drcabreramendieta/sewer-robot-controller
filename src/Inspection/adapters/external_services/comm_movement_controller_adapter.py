from Inspection.ports.output.movement_controller_port import MovementControllerPort
from Communication.ports.input import MovementServicePort
from Communication.domain.entities.wheels_entities import Rotation, Direction
from logging import Logger

class CommMovementControllerAdapter(MovementControllerPort):
    def __init__(self, robot:MovementServicePort, logger:Logger) -> None:
        super().__init__()
        self.robot = robot
        self.logger = logger
        self.value = 3
        
    def change_speed(self, value:int) -> None:
        self.value = value  

    def move_forward(self) -> None:
        self.robot.move(direction=Direction.FORWARD, rotation=Rotation.CENTER, speed=self.value)

    def move_backward(self) -> None:
        self.robot.move(direction=Direction.BACKWARD, rotation=Rotation.CENTER, speed=self.value)

    def rotate_left_forward(self) -> None:
        self.robot.move(direction=Direction.FORWARD, rotation=Rotation.LEFT, speed=self.value)

    def rotate_right_forward(self) -> None:
        self.robot.move(direction=Direction.FORWARD, rotation=Rotation.RIGHT, speed=self.value)

    def rotate_left_backward(self) -> None:
        self.robot.move(direction=Direction.BACKWARD, rotation=Rotation.LEFT, speed=self.value)

    def rotate_right_backward(self) -> None:
        self.robot.move(direction=Direction.BACKWARD, rotation=Rotation.RIGHT, speed=self.value)
        
    def stop(self) -> None:
        self.robot.move(direction=Direction.STOP, rotation=Rotation.CENTER, speed=0)