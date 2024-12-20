from dataclasses import dataclass


@dataclass
class ImageInfo:
    path: str
    capture_date_time: str


@dataclass
class RecordInfo:
    path: str
    stop_date_time: str
    start_date_time: int