import threading
import time
from logging import Logger
from typing import Callable, Optional

from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Communication.ports.output import TelemetryControllerPort


class MockCanTelemetryControllerAdapter(TelemetryControllerPort):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.callback: Optional[Callable[[TelemetryMessage], None]] = None
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._counter = 0

    def callback_setup(self, callback: Callable[[TelemetryMessage], None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        if self._thread and self._thread.is_alive():
            self.logger.info("Mock telemetry already running")
            return
        self.logger.info("Mock telemetry start_listening")
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop_listening(self) -> None:
        self.logger.info("Mock telemetry stop_listening")
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            if self.callback:
                message = self._build_ecu_message()
                self.callback(message)

                if self._counter % 3 == 0:
                    self.callback(self._build_motor_message())
            self._counter += 1
            time.sleep(0.5)

    def _build_ecu_message(self) -> TelemetryMessage:
        temperature = 20 + (self._counter % 15)
        humidity = 40 + (self._counter % 30)
        x_slop = (self._counter * 3) % 360
        y_slop = (self._counter * 5) % 360
        motor_status = 0xE0 if self._counter % 10 == 0 else 0xC0

        variables = {
            "Temperature": temperature,
            "Humidity": humidity,
            "X slop": x_slop,
            "Y slop": y_slop,
            "Motor status": motor_status,
        }
        return TelemetryMessage(
            message_type="ECU telemetry",
            variables=variables,
            timestamp=time.time(),
        )

    def _build_motor_message(self) -> TelemetryMessage:
        variables = {
            "revolution_counter": self._counter,
            "angular_position": (self._counter * 360 / 65535),
            "speed": (self._counter * 2) % 500,
            "current": (self._counter * 3) % 200,
        }
        return TelemetryMessage(
            message_type="motor telemetry",
            variables=variables,
            timestamp=time.time(),
        )
