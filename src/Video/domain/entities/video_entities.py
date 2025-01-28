from dataclasses import dataclass


@dataclass
class VideoMessage:
    """Video frame data container.

    Stores raw frame data from video capture devices.

    Attributes:
        frame (list): Raw frame data, typically numpy array from OpenCV
    """
    frame: list