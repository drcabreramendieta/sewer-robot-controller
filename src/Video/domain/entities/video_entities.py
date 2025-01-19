from dataclasses import dataclass
"""Video frame messaging entities.

This module defines data classes for representing video frame data
in the streaming pipeline.
"""

@dataclass
class VideoMessage:
    """Video frame data container.

    Stores raw frame data from video capture devices.

    Attributes:
        frame (list): Raw frame data, typically numpy array from OpenCV
    """
    frame: list