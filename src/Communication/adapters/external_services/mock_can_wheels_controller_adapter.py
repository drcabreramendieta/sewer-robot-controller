from logging import Logger

from Communication.domain.entities.wheels_entities import WheelsModule
from Communication.ports.output import WheelsControllerPort


class MockCanWheelsControllerAdapter(WheelsControllerPort):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def move(self, wheels_state: WheelsModule) -> None:
        self.logger.info("Mock wheels move: %s", wheels_state)
