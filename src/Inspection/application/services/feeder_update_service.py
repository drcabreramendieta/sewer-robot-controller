from Inspection.ports.input import FeederUpdateServicePort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
from Inspection.ports.ouput import FeederControllerPort, FeederObserverPort
from typing import List

class FeederUpdateService(FeederUpdateServicePort):
    """Service for managing feeder control updates and notifications.
    FeederUpdateService Implements observer pattern to coordinate feeder control operations
    and notify registered observers of state changes.

    Args:
        FeederUpdateServicePort (FeederUpdateServicePort): Base interface for feeder update operations
    """ 
    observers:List[FeederObserverPort]
    def __init__(self, feeder_controller:FeederControllerPort, observer:FeederObserverPort):
        """Initialize the feeder update service with controller and observer.
        
        __init__ Sets up the feeder update service with required dependencies and initializes
        the observer list. Registers the initial observer if provided.

        Args:
            feeder_controller (FeederControllerPort): Interface to control feeder hardware operations
                         and send commands to physical device
            observer (FeederObserverPort): Initial observer to receive feeder state updates and 
                 notifications about control changes
        Attributes:
            observer: Currently registered primary observer
            observers: List of all registered observers
            feeder_controller: Interface for hardware control operations
        """        
        super().__init__()
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer)
        self.feeder_controller = feeder_controller

    def register_observer(self, observer:FeederObserverPort):
        """
        register_observer Register new observer for feeder updates.

        Args:
            observer (FeederObserverPort): Observer instance to receive feeder state updates
        """        
        self.observers.append(observer)

    def update_feeder_control(self, feeder_control_data:FeederControlData) -> None:
        """
        update_feeder_control Update feeder control state and notify observers.

        Args:
            feeder_control_data (FeederControlData): New feeder control parameters
        """        
        self._notify(data=feeder_control_data)

    def _notify(self, data: FeederControlData):
        """
        _notify Notify all registered observers of feeder state change.

        Args:
            data (FeederControlData): Updated feeder control data to broadcast
        """        
        for observer in self.observers:
            observer.on_feeder_ready(data=data)
        
    def send_message(self, msg:str) -> None:
        """
        send_message Send control message to feeder hardware

        Args:
            msg (str): Control message to send to feeder
        """        
        self.feeder_controller.send_message(msg=msg)