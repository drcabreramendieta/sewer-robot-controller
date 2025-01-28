from Inspection.ports.ouput.movement_controller_port import MovementControllerPort
from Communication.ports.input import MovementServicePort
from Communication.domain.entities.wheels_entities import Rotation, Direction
from logging import Logger

class CommMovementControllerAdapter(MovementControllerPort):
    """Adapter for robot movement control through Communication service.

    Args:
        robot (MovementServicePort): Movement service for control operations
        logger (Logger): Logger instance for error and info logging

    Attributes:
        robot: Movement service instance
        logger: Logger instance
        value: Current movement speed value
    """

    def __init__(self, robot:MovementServicePort, logger:Logger) -> None:
        """Initialize movement controller adapter."""
        super().__init__()
        self.robot = robot
        self.logger = logger
        self.value = 3
        
    def change_speed(self, value:int) -> None:
        """Change robot movement speed.

        Args:
            value: New speed value
        """
        self.value = value  

    def move_forward(self) -> None:
        """Move robot forward in straight line."""
        self.robot.move(direction=Direction.FORWARD, rotation=Rotation.CENTER, speed=self.value)

    def move_backward(self) -> None:
        """Move robot backward in straight line."""
        self.robot.move(direction=Direction.BACKWARD, rotation=Rotation.CENTER, speed=self.value)

    def rotate_left_forward(self) -> None:
        """Move robot forward while rotating left."""
        self.robot.move(direction=Direction.FORWARD, rotation=Rotation.LEFT, speed=self.value)

    def rotate_right_forward(self) -> None:
        """Move robot forward while rotating right."""
        self.robot.move(direction=Direction.FORWARD, rotation=Rotation.RIGHT, speed=self.value)

    def rotate_left_backward(self) -> None:
        """Move robot backward while rotating left."""
        self.robot.move(direction=Direction.BACKWARD, rotation=Rotation.LEFT, speed=self.value)

    def rotate_right_backward(self) -> None:
        """Move robot backward while rotating right."""
        self.robot.move(direction=Direction.BACKWARD, rotation=Rotation.RIGHT, speed=self.value)
        
    def stop(self) -> None:
        """Stop all robot movement."""
        self.robot.move(direction=Direction.STOP, rotation=Rotation.CENTER, speed=0)