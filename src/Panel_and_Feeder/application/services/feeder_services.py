from Panel_and_Feeder.ports.input import FeederServicesPort
from Panel_and_Feeder.ports.output.feeder_observer_port import FeederObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
from Panel_and_Feeder.ports.output.panel_and_feeder_controller_port import PanelAndFeederControllerPort
from logging import Logger
from typing import List

class FeederServices(FeederServicesPort):
    """Service for managing feeder operations and notifications.

    Implements feeder control services including observer pattern for
    updates and message-based control.

    Args:
        paf_controller (PanelAndFeederControllerPort): Hardware controller
        logger (Logger): Logger instance for operations
        observer (FeederObserverPort): Initial observer for updates

    Attributes:
        observers (List[FeederObserverPort]): List of registered observers
        paf_controller (PanelAndFeederControllerPort): Hardware control interface
        logger (Logger): Operations logger
    """
    observers:List[FeederObserverPort]
    def __init__(self, paf_controller:PanelAndFeederControllerPort, logger:Logger, observer:FeederObserverPort) -> None:
        """Initialize feeder services with controller and observer.

        Args:
            paf_controller (PanelAndFeederControllerPort): Hardware controller interface
            logger (Logger): Logger for operation tracking 
            observer (FeederObserverPort): Initial update observer

        Raises:
            ValueError: If controller or logger is None
        """
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer)
        self.paf_controller = paf_controller
        self.logger = logger
        self.paf_controller.feeder_callback_setup(self._notify_feeder_control_data)
        super().__init__()


    def _notify_feeder_control_data(self, feeder_control_data:FeederControlData) -> None:
        """Notify all observers of feeder control updates.

        Args:
            feeder_control_data (FeederControlData): Updated control state 

        Raises:
            RuntimeError: If notification fails
        """
        for observer in self.observers:
            observer.on_feeder_control_data_ready(feeder_control_data=feeder_control_data)

    def register_observer(self, observer:FeederObserverPort):
        """Register new observer for feeder updates.

        Args:
            observer (FeederObserverPort): Observer to receive updates

        Raises:
            ValueError: If observer is None
        """
        self.observers.append(observer)

    def start_listening(self):
        """Start listening for feeder control updates.

        Raises:
            RuntimeError: If listening fails to start
        """
        print('start')
        self.paf_controller.start_listening()

    def stop_listening(self):
        """Stop listening for feeder control updates.

        Raises:
            RuntimeError: If listening fails to stop
        """
        self.paf_controller.stop_listening()

    def send_message(self, message:str):
        """Send control message to feeder hardware.

        Args:
            message (str): Control message to send

        Raises:
            RuntimeError: If message sending fails
            ValueError: If message is empty
        """ 
        self.paf_controller.send_message(message)