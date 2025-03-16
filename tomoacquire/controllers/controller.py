
from tomoacquire.states import MicroscopeState
# singleton class 
class TomoacquireController(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(TomoacquireController, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self):
        self.state = MicroscopeState.DISCONNECTED
        pass
    

    def connect(self, microscope):
        self.states = MicroscopeState.CONNECTED
        self.microscope = microscope


TOMOACQUIRE_CONTROLLER = TomoacquireController()