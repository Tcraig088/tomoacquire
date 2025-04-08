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

class Controller(Connection):
    def __init__(self):
        self._state = MicroscopeState.Disconnected
        self.isscanwidget = False
        self.istiltselected = False

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

    def _show_imaging_settings(self):
        if not self.isscanwidget:
            scan_detector_dropdown = widgets.SelectMultiple(options = self.microscope.detector_options, description='Scan Detectors:')
            acquire_detector_dropdown = widgets.SelectMultiple(options = self.microscope.detector_options, description='Acquire Detectors:')

            scan_dwell = widgets.FloatText(value=1.0, description='Dwell Time (us):')
            scan_frame = widgets.IntText(value=1024, description='Frame Size:')
            scan_exptime = widgets.FloatText(value=0.0, description='Exposure Time (s):')

            acquire_dwell = widgets.FloatText(value=2.0, description='Dwell Time (us):')
            acquire_frame = widgets.IntText(value=1024, description='Frame Size:')
            acquire_exptime = widgets.FloatText(value=0.0, description='Exposure Time (s):')


            imaging_button = widgets.Button(description='Update Imaging Settings')
            

            magnification_select = widgets.IntSlider(value = int(self.microscope.get_magnification_index()), 
                                    min=0, 
                                    max=len(self.microscope.magnification_options)-1, 
                                    description='Magnification:')
            
            isblanked_select = widgets.Checkbox(value=self.microscope.isblank, description='Blank Beam')

            isblanked_select.observe(self._on_blank, names='value')
            magnification_select.observe(self._on_magnification, names='value')
            imaging_button.on_click(self._on_ready)

            self.detect_group = widgets.HBox([scan_detector_dropdown, acquire_detector_dropdown])
            self.scan_group = widgets.HBox([scan_dwell, scan_frame, scan_exptime])
            self.acquire_group = widgets.HBox([acquire_dwell, acquire_frame, acquire_exptime])
            self.control_group = widgets.HBox([magnification_select, isblanked_select])

            self.imaging_group = widgets.VBox([self.detect_group, self.scan_group, self.acquire_group, self.control_group, imaging_button])
            display(self.imaging_group)
            self.isscanwidget = True

    def show(self):
        match self.state:
            case MicroscopeState.Disconnected:
                microscopes_dropdown = widgets.Dropdown(options = mc.get_names())
                connect_button = widgets.Button(description='Connect')
                self.connect_group = widgets.HBox([microscopes_dropdown, connect_button])
                connect_button.on_click(self._on_connect)
                display(self.connect_group)
                
            case MicroscopeState.Connected :
                self._show_imaging_settings()

            case MicroscopeState.Ready:
                self._show_imaging_settings()
                self.microscope.image.show()

                tiltscheme = widgets.Dropdown(options = TOMOBASE_TILTSCHEMES.keys(), description='Tilt Scheme:')
                tiltscheme_select = widgets.Button(description='Select')
                self.tiltscheme_group = widgets.HBox([tiltscheme, tiltscheme_select])

                experiment = widgets.Dropdown(options = ['Tomography', 'Callibration'], description='Experiment:')
                self.experiment_group = widgets.HBox([experiment, self.tiltscheme_group])

                display(self.experiment_group)
                tiltscheme_select.on_click(self._on_tiltscheme)

                useprediction = widgets.Checkbox(value=False, description='Use Prediction')
                correctbacklash = widgets.Checkbox(value=True, description='Correct Backlash')
                automate = widgets.Checkbox(value=False, description='Automate')
                interem_tilts = widgets.FloatText(value=90.0, description='Intermediate Tilt:')
                correct_intermediates = widgets.Checkbox(value=False, description='Correct Intermediate Tilt')  
                interem_pause = widgets.FloatText(value=0.0, description='Intermediate Pause:')

                

                


    def _on_tiltscheme(self, b):
        if self.istiltselected:
            self.tiltwidget.close()
        self.istiltselected = True
        self.tiltwidget = TOMOBASE_TILTSCHEMES[self.tiltscheme_group.children[0].value].controller.TiltSchemeWidget()
        display(self.tiltwidget)


    def _on_magnification(self, b):
        if self.state == MicroscopeState.Ready:
            self.threadedrequest(self.set_magnification, self.control_group.children[0].value)

    def set_magnification(self, magnification):
            self.microscope.magnification = magnification

    def _on_blank(self, b):
        print(self.state)
        if self.state == MicroscopeState.Ready:
            self.threadedrequest(self.set_blank, self.control_group.children[1].value)
    
    def set_blank(self, isblanked):
        self.microscope.isblank = isblanked

    def _on_ready(self, b):
        if self.state == MicroscopeState.Connected:
            self.imaging_group.children[4].description = 'Update'

        scan_dwell = self.scan_group.children[0].value *10**-6
        scan_frame = self.scan_group.children[1].value
        scan_exptime = self.scan_group.children[2].value
        if scan_exptime == 0.0:
            scan_exptime = scan_dwell * scan_frame**2
        
        acquire_dwell = self.acquire_group.children[0].value *10**-6
        acquire_frame = self.acquire_group.children[1].value
        acquire_exptime = self.acquire_group.children[2].value
        if acquire_exptime == 0.0:
            acquire_exptime = acquire_dwell * acquire_frame**2
        
        _dict = {
            'scan_detectors': self.detect_group.children[0].value,
            'scan_dwell': scan_dwell,
            'scan_frame': scan_frame,
            'scan_exptime': scan_exptime,

            'dwell_detectors': self.detect_group.children[1].value,
            'acquire_dwell': acquire_dwell,
            'acquire_frame': acquire_frame,
            'acquire_exptime': acquire_exptime, 
        }
        if self.state == MicroscopeState.Ready:
            _dict['magnification'] = self.microscope.magnification_options[self.control_group.children[0].value]
            _dict['isblanked'] = self.control_group.children[1].value

        self.setup_imaging_settings(**_dict)
    
    def setup_imaging_settings(self, **kwargs): 
        if self.state == MicroscopeState.Connected:
            kwargs['scan_exptime'] = kwargs.get('scan_exptime', kwargs['scan_dwell'] * kwargs['scan_frame']**2)
            kwargs['acquire_exptime'] = kwargs.get('acquire_exptime', kwargs['acquire_dwell'] * kwargs['acquire_frame']**2)
            self.microscope._set_imaging_settings(**kwargs) 
            self.state = MicroscopeState.Ready
            self.show()
        else:
            self.microscope._set_imaging_settings(**kwargs)

    def _on_connect(self, b):
        microscope_name = self.connect_group.children[0].value
        if self.state == MicroscopeState.Disconnected:
            self.connect(microscope_name)
            self.show()
            self.connect_group.children[1].description = 'Connected'
        

    def connect(self, microscope_name):
        self.microscope = mc.get_microscope(microscope_name)
        self.state = MicroscopeState.Connected

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
        print('executing')

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
                print('áttempt failed')
                time.sleep(0.1)









    


