from Communication.ports.input import MovementServicePort
from Communication.domain.entities.wheels_entities import Direction, Rotation, WheelsModule
from Communication.ports.output import WheelsControllerPort

class MovementService(MovementServicePort):
    """Service class for managing robot movement operations.

    This class implements the MovementServicePort interface and provides
    methods to control robot movement through a wheels controller.

    Args:
        wheels_controller (WheelsControllerPort): Controller for wheels operations

    Attributes:
        wheels_controller: Interface to control wheel hardware
    """
    def __init__(self, wheels_controller:WheelsControllerPort):
        """Initialize movement service with wheels controller."""
        super().__init__()
        self.wheels_controller = wheels_controller

    def move(self, direction:Direction, rotation:Rotation, speed:int) -> None:
        """Control robot movement by setting wheel parameters.

        Args:
            direction: Movement direction (FORWARD, BACKWARD, STOP)
            rotation: Rotation direction (LEFT, RIGHT, NONE)
            speed: Movement speed value (0-100)
        """
        wheels_state = WheelsModule(direction=direction, 
                                    rotation=rotation, 
                                    speed=speed)
        self.wheels_controller.move(wheels_state=wheels_state)