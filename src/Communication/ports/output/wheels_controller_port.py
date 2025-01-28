from abc import ABC, abstractmethod
from Communication.domain.entities.wheels_entities import WheelsModule

class WheelsControllerPort(ABC):
    """Abstract interface for wheels hardware control.

    This interface defines the required methods for implementing
    low-level wheel control functionality.
    """

    @abstractmethod   
    def move(self, wheels_state:WheelsModule) -> None:
        """Control robot wheel movement.

        Args:
            wheels_state: Configuration for wheels movement including
                        direction, rotation and speed
        """
        pass
