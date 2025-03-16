import temscript
import time
import enum
from tomobase.log import logger
from tomoacquire.scanwindow import ScanWindow
from threading import Thread
import numpy as np

class MicroscopeState(enum.Enum):
    Connected = 0
    Disconnected = 1
    Callibration = 2
    Tomography = 3

           
class AcquisitionController():
    def __init__(self, microscope):
        self.detectors = []
        self._isscan = True
        
    @property
    def isscan(self):
        return self._isscan
    
    @isscan.setter
    def isscan(self, isscan):
        self._isscan = isscan

class Controller():
    def __init__(self, file):
        
        filename = file
        with open(filename, 'r') as f:
            json = json.load(f)
        
        # getmicroscope information for setting up the connection
        microscope_class = microscopes.get_microscope(json['Microscope Type'])
        self.microscope = microscope_class(json['address'], json['reply port'], json['subscribe port'])
        
        self._state = MicroscopeState.Connected
        self.magnifications = self.microscope.get_mag_list()
        self.detectors = self.microscope.get_detectors()
        
        # Generally this should be set by the microscope
        # however there can be inaccuracy in the beam current read out or temscript call
        self._beam_current = self.microscope.get_beam_current()
        self.acquisition.isscan = True
        self.stage = StageController(self.microscope)

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        if self._state == state:
            logger.warning(f'Already in state {state}. Cannot Change Experimental State.')

        match state:
            case MicroscopeState.Connected:
                self.acquisition.isscan = True
                self.stage.reset()
                self._state = state
            case MicroscopeState.Disconnected:
                while self._state != MicroscopeState.Disconnected:
                    if self._state == MicroscopeState.Connected:
                        self.stage.reset()
                        self.stage.stop()
                        self._state = state
                    else:
                        self._state = MicroscopeState.Connected
            case MicroscopeState.Callibration:
                if self._state != MicroscopeState.Connected:
                    logger.error(f'Cannot enter {state} state without first connecting to microscope. Either the Micrsocope is not connected or their is a currently active experiment running')
                else:
                    self._state = state
            case MicroscopeState.Tomography:
                if self._state != MicroscopeState.Connected:
                    logger.error(f'Cannot enter {state} state without first connecting to microscope. Either the Micrsocope is not connected or their is a currently active experiment running')
                else:
                    self._state = state

    def connect(self, detectors=[], 
                scan_window=1024, 
                scan_dwell=1*10**-6, 
                scan_exptime=0.0, 
                acquire_window=1024,
                acquire_dwell=1*10**-6,
                acquire_exptime=0.0):
        
        if scan_exptime == 0.0:
            scan_exptime = scan_window * scan_dwell *scan_window
        if acquire_exptime == 0.0:
            acquire_exptime = acquire_window * acquire_dwell * acquire_window

        self.microscope.setup(detectors, scan_window, scan_dwell, scan_exptime, acquire_window, acquire_dwell, acquire_exptime)
        self._state = MicroscopeState.Connected
        self._scan_window = ScanWindow()
        self._scan_window.show()
        

    def starttomo(self, tiltscheme, detectors, magnifications):
        self.state = MicroscopeState.Tomography
        self.tiltscheme = tiltscheme
        
        self.stage.move(tiltscheme.get_angle())
          
    def getimages():
        pass



