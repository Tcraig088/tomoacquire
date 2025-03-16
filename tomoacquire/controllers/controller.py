from tomoacquire.states import MicroscopeState
from qtpy.QtCore import Signal, QObject
# singleton class 
class TomoacquireController(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(TomoacquireController, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self):
        super().__init__()
        self.state = MicroscopeState.DISCONNECTED
        pass
    
    def connect(self, microscope):
        self.states = MicroscopeState.CONNECTED
        self.microscope = microscope

    def set_scan(self, scan_dict):
        self.microscope.set_scan(scan_dict)

    def set_acquisition(self, acquisition_dict):
        self.microscope.set_acquisition(acquisition_dict)

    def set_detectors(self, detectors):
        self.microscope.set_detectors(detectors)

    def start_scan(self):
        self.microscope.start_scan()



TOMOACQUIRE_CONTROLLER = TomoacquireController()