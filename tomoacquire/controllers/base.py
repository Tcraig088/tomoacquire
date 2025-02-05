import time
import enum
from ipywidgets import widgets
from IPython.display import display
from threading import Thread
from tomobase.log import logger
from tomoacquire.scanwindow import ScanWindow
from tomoacquire import microscope_config as mc
from threading import Thread
import numpy as np
import stackview

class MicroscopeState(enum.Enum):
    Connected = 0
    Disconnected = 1
    Callibration = 2
    Tomography = 3
    Imaging = 4

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
            case MicroscopeState.Imaging:
                if self._state != MicroscopeState.Connected:
                    logger.error(f'Cannot enter {state} state without first connecting to microscope. Either the Micrsocope is not connected or their is a currently active experiment running')
                else:
                    self._state = state

    def show(self):
        # Connection Options
        
        new_microscope_name = widgets.Text(value='New Microscope',
                                  description='Name:'
                                  )
        new_microscope_address = widgets.Text(value='localhost',
                                  description='Address:'
                                  )
        new_microscope_port = widgets.IntText(value=50000,
                                    description='Port:'
                                    )
        new_microscope_type = widgets.Dropdown(options = mc.get_types(),
                                    description='Type:'
                                    )
        n_magnifications = widgets.IntText(value=1,
                                    description='Number of Magnifications:'
                                    )
        detector_pixelsize = widgets.FloatText(value=1.0,
                                    description='Detector Pixel Size (nm):'
                                    )
                                           
        save_button = widgets.Button(description='Save')

        self.new_microscope_group = widgets.GridBox([new_microscope_name, new_microscope_address, new_microscope_port, new_microscope_type, n_magnifications, detector_pixelsize, save_button])
        save_button.on_click(self._on_save)

        dropdown = widgets.Dropdown(options = mc.get_names())
        connect_button = widgets.Button(description='Connect')

        self.connect_group = widgets.HBox([dropdown, connect_button])
        connect_button.on_click(self._on_connect)

        display(widgets.VBox([self.new_microscope_group, self.connect_group]))
        

    def show_imaging(self):
        dropdown = widgets.SelectMultiple(options = self.microscope.detectors,
                                          description='Detectors:')
        
        magnification = widgets.IntSlider(value = int(self.microscope.get_magnification_index()), 
                                          min=0, 
                                          max=self.microscope.magnifications_total-1, 
                                          description='Magnification:')

        magnification.observe(self._on_magnification)

        scan_dwell = widgets.FloatText(value=1.0,
                                        description='Dwell Time (us):')
        scan_frame = widgets.IntText(value=1024,
                                     description='Frame Size:')
        scan_exptime = widgets.FloatText(value=0.0,
                                         description='Exposure Time (s):')
        
        self.scan_group = widgets.HBox([scan_dwell, scan_frame, scan_exptime])

        acquire_dwell = widgets.FloatText(value=2.0,
                                        description='Dwell Time (us):')
        acquire_frame = widgets.IntText(value=1024,
                                        description='Frame Size:')
        acquire_exptime = widgets.FloatText(value=0.0,
                                         description='Exposure Time (s):')
        self.acquire_group = widgets.HBox([acquire_dwell, acquire_frame, acquire_exptime])

        imaging_button = widgets.Button(description='Update Imaging Settings')
        imaging_button.on_click(self._on_imaging)

        self.imaging_group = widgets.VBox([dropdown, magnification, self.scan_group, self.acquire_group, imaging_button])
        display(self.imaging_group)

    def _on_magnification(self, b):
        self.microscope.magnification = self.imaging_group.children[1].value

    def _on_imaging(self, b):
        detectors = self.imaging_group.children[0].value
        print(detectors)
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

        print(self.state)
        if self.state == MicroscopeState.Connected:
            self.microscope.imaging_settings(detectors, scan_dwell, scan_frame, scan_exptime, acquire_dwell, acquire_frame, acquire_exptime) 
            self._state = MicroscopeState.Imaging
            self.microscope.isscan = True
            acq_thread = Thread(target=self.acquire)
            acq_thread.start()

    def acquire(self):
        self.microscope.acquire()

    def _on_save(self, b):
        name = self.new_microscope_group.children[0].value
        address = self.new_microscope_group.children[1].value
        port = self.new_microscope_group.children[2].value
        mtype = self.new_microscope_group.children[3].value
        n_magnifications = self.new_microscope_group.children[4].value
        detector_pixelsize = self.new_microscope_group.children[5].value
        print(mtype)
        mc.add_microscope(name, address, port, mtype, n_magnifications, detector_pixelsize)
        
        dropdown = self.connect_group.children[0]
        dropdown.options = mc.get_names()
        dropdown.value = name

    def _on_connect(self, b):
        microscope_name = self.connect_group.children[0].value
        self.connect(microscope_name)
        self.show_imaging()
        #self.show_experiment()

    def connect(self, microscope_name):
        self.microscope = mc.get_microscope(microscope_name)
        self.state = MicroscopeState.Connected







    


