from dataclasses import dataclass

@dataclass
class TelemetryMessage:
    message_type: str
    variables: dict
    timestamp : float
