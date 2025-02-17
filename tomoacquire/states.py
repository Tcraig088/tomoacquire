import enum

class MicroscopeState(enum.Enum):
    Connected = 0
    Disconnected = 1
    Callibration = 2
    Tomography = 3
    Ready = 4

class ImagingState(enum.Enum):
    Idle = 0
    Blocked = 1
    Requested = 2
    Queued = 3
    Executing = 4