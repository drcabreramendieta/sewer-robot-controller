from Communication.ports.observer import TelemetryObserver
from Communication.domain.entities import TelemetryMessage

class TestTelemetryObserver(TelemetryObserver):
    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        print('observer:',telemetry)