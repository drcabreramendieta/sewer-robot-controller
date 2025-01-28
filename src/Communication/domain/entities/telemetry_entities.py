from dataclasses import dataclass
@dataclass
class TelemetryMessage:
    """Container for telemetry data messages.

    This class represents a single telemetry message with its type,
    associated variables and timestamp.

    Attributes:
        message_type (str): Type of telemetry message ('motor telemetry' or 'ECU telemetry')
        variables (dict): Dictionary of telemetry variables and their values
        timestamp (float): Unix timestamp of when the message was created


    """
    
    message_type: str
    variables: dict
    timestamp : float
