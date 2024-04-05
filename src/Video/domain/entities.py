from dataclasses import dataclass
from enum import IntEnum

@dataclass
class VideoMessage:
    frame: list

class DvrOrder(IntEnum):
    START_RECORDING = 1
    STOP_RECORDING = 2
    TAKE_PHOTO = 3
    GET_VIDEO = 4
    GET_PHOTO = 5

@dataclass
class ImageInfo:
    path: str
    capture_date_time: str
    

@dataclass
class RecordInfo:
    path: str
    stop_date_time: str
    start_date_time: int
    
    

