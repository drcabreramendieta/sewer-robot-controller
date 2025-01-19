from enum import IntEnum
"""DVR control command entities.

This module defines enumerations for DVR control operations including
recording, photo capture and content retrieval commands.
"""
class DvrOrder(IntEnum):
    """DVR control command enumeration.

    Defines available DVR control operations with integer values.

    Attributes:
        START_RECORDING (1): Begin video recording
        STOP_RECORDING (2): Stop current recording
        TAKE_PHOTO (3): Capture single frame
        GET_VIDEO (4): Retrieve recorded video
        GET_PHOTO (5): Retrieve captured photo
    """
    START_RECORDING = 1
    STOP_RECORDING = 2
    TAKE_PHOTO = 3
    GET_VIDEO = 4
    GET_PHOTO = 5

    
    

