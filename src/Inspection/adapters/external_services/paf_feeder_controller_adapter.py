from Inspection.ports.ouput import FeederControllerPort
from Panel_and_Feeder.ports.input import FeederServicesPort
"""Panel and Feeder controller adapter implementation.

This module provides an adapter that implements the FeederControllerPort interface
for controlling feeder operations through the Panel and Feeder services.
"""
class PafFeederControllerAdapter(FeederControllerPort):
    """Adapter for feeder control through Panel and Feeder services.

    This adapter implements the FeederControllerPort interface to control
    feeder operations using the Panel and Feeder service layer.

    Args:
        feeder_services (FeederServicesPort): Service for feeder operations

    Attributes:
        feeder_services: Interface to feeder control services
    """
    def __init__(self, feeder_services:FeederServicesPort):
        """Initialize feeder controller adapter."""
        super().__init__()
        self.feeder_services = feeder_services

    def send_message(self, msg:str) -> None:
        """Send control message to feeder.

        Args:
            msg: Control message to be sent to feeder
        """
        self.feeder_services.send_message(message=msg)