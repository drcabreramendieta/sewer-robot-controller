from Communication.ports.observer import TelemetryObserver
from Communication.domain.entities import Telemetry

class TestTelemetryObserver(TelemetryObserver):
    def on_telemetry_ready(self, telemetry:Telemetry) -> None:
        print(telemetry)