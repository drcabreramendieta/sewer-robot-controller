import sys
import pytest
from unittest.mock import MagicMock
import time

# PyQt6 imports
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject

# python-can imports
import can

from Inspection.ports.input import TelemetryUpdateServicePort
from Communication.application.services import TelemetryServices
from Communication.adapters.external_services import PyqtTelemetryObserverAdapter, CanTelemetryControllerAdapter

@pytest.fixture(scope="module")
def qapp():
    app = QApplication(sys.argv)
    yield app

def test_telemetry_integration(qapp, qtbot):
    logger = MagicMock(name='Logger')
    mock_telemetry_update_service = MagicMock(spec=TelemetryUpdateServicePort)

    bus = can.Bus(interface='virtual', receive_own_messages=True)

    telemetry_can_adapter = CanTelemetryControllerAdapter(bus,logger)

    observer = PyqtTelemetryObserverAdapter(mock_telemetry_update_service,logger)
    service = TelemetryServices(telemetry_can_adapter,logger,observer)
    service.start_listening()
    try:
        test_data = [1, 2, 3, 4, 5, 6, 7, 8]
        msg = can.Message(arbitration_id=0x400, data=test_data, is_extended_id=False)

        bus.send(msg)

        with qtbot.waitSignal(observer.pyqt_signal_connect.telemetry_updated_signal, timeout=5000) as blocker:
            blocker.wait()

        mock_telemetry_update_service.update_telemetry.assert_called_once()

    finally:
        service.stop_listening()
        bus.shutdown()
