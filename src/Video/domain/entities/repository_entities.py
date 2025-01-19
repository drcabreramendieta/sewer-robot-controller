from dataclasses import dataclass
"""Repository data entities.

This module defines data classes for representing stored image and
recording information in the repository.
"""

@dataclass
class ImageInfo:
    """Image capture information.

    Stores path and timestamp for captured images.

    Attributes:
        path (str): Filesystem path to image file
        capture_date_time (str): Capture timestamp
    """
    path: str
    capture_date_time: str


@dataclass
class RecordInfo:
    """Video recording information.

    Stores path and timing information for video recordings.

    Attributes:
        path (str): Filesystem path to video file
        stop_date_time (str): Recording end timestamp (format: YYYYMMDD_HHMMSS)
        start_date_time (int): Recording start timestamp (format: YYYYMMDD_HHMMSS)
    """
    path: str
    stop_date_time: str
    start_date_time: int