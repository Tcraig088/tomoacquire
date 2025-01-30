import temscript
import time
import enum
from tomobase.log import logger

from tomoacquire.scanwindow import ScanWindow

class MicroscopeState(enum.Enum):
    Connected = 0
    Disconnected = 1
    Callibration = 2
    Tomography = 3

class StageController():
    def __init__(self, microscope):
        self.microscope = microscope

        self._automate = False
        self._speed = 0.0
        self._pause_long = 0.0
        self._pause_short = 0.0
        self._high_tilt = 90.0
        self._intermediate_tilt = 90.0
        self._intermediate_pause_time = 0.0

        self._useprediction = False
        self._use_interem_prediction = False
        self._confidence = 10

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

        # getmicroscope information for setting up the connection
        self.microscope = FEIMicroscope('localhost')
        self._state = MicroscopeState.Connected

        self.magnifications = self.microscope.get_mag_list()
        self.detectors = self.microscope.get_detectors()
        # Generally this should be set by the microscope
        # however there can be inaccuracy in the beam current read out or temscript call
        self._beam_current = self.microscope.get_beam_current()

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
        self.mode
        self._scan_window = ScanWindow()
        self._scan_window.show()


    def precalibrate()







    def acquire(self):
        while self._active:
            images = self.microscope.acquire()
            self._scan_window.data = images
            if 






    def start_tomo(self, confidence=4):
        
        self.magnification = 


        self._time_start = time.time()




        pass




class FEIMicroscope:
    def __init__(self, file):
        


        if address == 'localhost':
            self.tem = temscript.NullMicroscope(True)
        else:
            self.tem = temscript.RemoteMicroscope(address)

        
    def 