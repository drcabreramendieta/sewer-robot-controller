from logging import Logger
from typing import Callable, Optional

from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Communication.ports.output import TelemetryControllerPort


class MockCanTelemetryControllerAdapter(TelemetryControllerPort):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.callback: Optional[Callable[[TelemetryMessage], None]] = None

    def callback_setup(self, callback: Callable[[TelemetryMessage], None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        self.logger.info("Mock telemetry start_listening")

    def stop_listening(self) -> None:
        self.logger.info("Mock telemetry stop_listening")
