import enum

class MicroscopeState(enum.Enum):
    CONNECTED = 0
    DISCONNECTED = 1
    CALLIBRATION = 2
    TOMOGRAPHY = 3
    DETECTORSINIT= 4

class ImagingState(enum.Enum):
    Idle = 0
    Blocked = 1
    Requested = 2
    Queued = 3
    Executing = 4