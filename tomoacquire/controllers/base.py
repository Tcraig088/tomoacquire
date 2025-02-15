import time
import enum
from ipywidgets import widgets
from IPython.display import display
from threading import Thread
from tomobase.log import logger
from tomoacquire.scanwindow import ScanWindow
from tomoacquire import config as mc
from threading import Thread
import numpy as np
import stackview
from tomobase.registrations.tiltschemes import TOMOBASE_TILTSCHEMES
from tomoacquire.states import MicroscopeState, ImagingState
from tomobase.log import logger

class BaseController():
    def __init__(self):
        self._state = MicroscopeState.Disconnected
        self.microscope = None
        
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        if self._state == state:
            logger.warning(f'Already in state {state}. Cannot Change Experimental State.')

        match state:
            case MicroscopeState.Connected:
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
            case MicroscopeState.Ready:
                if self._state != MicroscopeState.Connected:
                    logger.error(f'Cannot enter {state} state without first connecting to microscope. Either the Micrsocope is not connected or their is a currently active experiment running')
                else:
                    self._state = state

    def threadedrequest(self, func, *args, **kwaargs):
        args = (func, *args)
        thread = Thread(target=self.processrequest, args=args, kwargs=kwaargs)
        thread.daemon = True
        thread.start()

    def processrequest(self, func, *args, **kwaargs):
        if self.microscope.state == ImagingState.Idle:
            self.microscope.state = ImagingState.Requested
        else:
            self.microscope.state = ImagingState.Queued

        while self.microscope.state != ImagingState.Queued:
            if self.state != ImagingState.Requested | self.state != ImagingState.Queued:
                self.state = ImagingState.Requested
            time.sleep(0.1)

        isexecute = True
        while isexecute:    
            try:
                self.microscope.state = ImagingState.Executing
                blanked = self.microscope.isblank
                self.microscope.isblank = True
                func(*args, **kwaargs)
                self.microscope.isblank = self.control_group.children[1].value
                isexecute = False
                self.microscope.state = ImagingState.Idle
            except Exception as e:
                logger.debug('Queue held open by another process')
                time.sleep(0.1)


   