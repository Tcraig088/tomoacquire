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

class MicroscopeState(enum.Enum):
    Connected = 0
    Disconnected = 1
    Callibration = 2
    Tomography = 3
    ScanConnected = 4

class Controller():
    def __init__(self):
        self._state = MicroscopeState.Disconnected

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
            case MicroscopeState.ScanConnected:
                if self._state != MicroscopeState.Connected:
                    logger.error(f'Cannot enter {state} state without first connecting to microscope. Either the Micrsocope is not connected or their is a currently active experiment running')
                else:
                    self._state = state

    def show(self):
        match self.state:
            case MicroscopeState.Disconnected:
                microscopes_dropdown = widgets.Dropdown(options = mc.get_names())
                connect_button = widgets.Button(description='Connect')
                self.connect_group = widgets.HBox([microscopes_dropdown, connect_button])
                connect_button.on_click(self._on_connect)
                display(self.connect_group)
                
            case MicroscopeState.Connected:
                detector_dropdown = widgets.SelectMultiple(options = self.microscope.detector_options, description='Detectors:')
                magnification_select = widgets.IntSlider(value = int(self.microscope.get_magnification_index()), 
                                          min=0, 
                                          max=len(self.microscope.magnification_options)-1, 
                                          description='Magnification:')

                scan_dwell = widgets.FloatText(value=1.0, description='Dwell Time (us):')
                scan_frame = widgets.IntText(value=1024, description='Frame Size:')
                scan_exptime = widgets.FloatText(value=0.0, description='Exposure Time (s):')
        
                self.scan_group = widgets.HBox([scan_dwell, scan_frame, scan_exptime])

                acquire_dwell = widgets.FloatText(value=2.0, description='Dwell Time (us):')
                acquire_frame = widgets.IntText(value=1024, description='Frame Size:')
                acquire_exptime = widgets.FloatText(value=0.0, description='Exposure Time (s):')
                
                self.acquire_group = widgets.HBox([acquire_dwell, acquire_frame, acquire_exptime])
                imaging_button = widgets.Button(description='Update Imaging Settings')
                
                magnification_select.observe(self._on_magnification, names='value')
                imaging_button.on_click(self._on_imaging)

                self.imaging_group = widgets.VBox([detector_dropdown, magnification_select, self.scan_group, self.acquire_group, imaging_button])
                display(self.imaging_group)

    def _on_magnification(self, b):
        self.microscope.magnification = self.imaging_group.children[1].value

    def _on_imaging(self, b):
        detectors = self.imaging_group.children[0].value
  
        scan_dwell = self.scan_group.children[0].value *10**-6
        scan_frame = self.scan_group.children[1].value
        scan_exptime = self.scan_group.children[2].value

        if scan_exptime == 0.0:
            scan_exptime = scan_frame * scan_dwell * scan_frame

        acquire_dwell = self.acquire_group.children[0].value *10**-6
        acquire_frame = self.acquire_group.children[1].value
        acquire_exptime = self.acquire_group.children[2].value

        if acquire_exptime == 0.0:
            acquire_exptime = acquire_frame * acquire_dwell * acquire_frame

        if self.state == MicroscopeState.Connected:
            self.microscope.imaging_settings(detectors, scan_dwell, scan_frame, scan_exptime, acquire_dwell, acquire_frame, acquire_exptime) 
            self._state = MicroscopeState.ScanConnected
            self.microscope.isscan = True
            acq_thread = Thread(target=self.acquire)
            acq_thread.daemon = True
            acq_thread.start()
            

    def acquire(self):
        self.microscope.acquire()
        


    def _connect_scanwindow(self, b):
        scan_dwell = self.scan_group.children[0].value *10**-6
        scan_frame = self.scan_group.children[1].value
        scan_exptime = self.scan_group.children[2].value
        if scan_exptime == 0.0:
            scan_exptime = self.scan_group.children[1].value * self.scan_group.children[0].value * self.scan_group.children[1].value
        
        acquire_dwell = self.acquire_group.children[0].value *10**-6
        acquire_frame = self.acquire_group.children[1].value
        acquire_exptime = self.acquire_group.children[2].value
        if acquire_exptime == 0.0:
            acquire_exptime = self.acquire_group.children[1].value * self.acquire_group.children[0].value * self.acquire_group.children[1].value
        
        _dict = {
            'detectors': self.imaging_group.children[0].value,
            'scan_dwell': scan_dwell,
            'scan_frame': scan_frame,
            'scan_exptime': scan_exptime,
            'acquire_dwell': acquire_dwell,
            'acquire_frame': acquire_frame,
            'acquire_exptime': acquire_exptime 
        }
        



    def _on_connect(self, b):
        microscope_name = self.connect_group.children[0].value
        self.connect(microscope_name)
        self.show()
        #self.show_experiment()

    def connect(self, microscope_name):
        self.microscope = mc.get_microscope(microscope_name)
        self.state = MicroscopeState.Connected







    


