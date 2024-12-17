from Communication.ports.input import MovementServicePort
from Communication.domain.entities.wheels_entities import Direction, Rotation, WheelsModule
from Communication.ports.output import WheelsControllerPort

class MovementService(MovementServicePort):
    def __init__(self, wheels_controller:WheelsControllerPort):
        super().__init__()
        self.wheels_controller = wheels_controller

    def move(self, direction:Direction, rotation:Rotation, speed:int) -> None:
        wheels_state = WheelsModule(direction=direction, 
                                    rotation=rotation, 
                                    speed=speed)
        self.wheels_controller.move(wheels_state=wheels_state)