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

from tomoacquire.controllers.base import BaseController

class ScanController(BaseController):
    def __init__(self):
        super().__init__()

    def _show_detectors(self):
        scan_detector_dropdown = widgets.SelectMultiple(options = self.microscope.detector_options, description='Scan Detectors:')
        acquire_detector_dropdown = widgets.SelectMultiple(options = self.microscope.detector_options, description='Acquire Detectors:')
        self.detect_group = widgets.HBox([scan_detector_dropdown, acquire_detector_dropdown])
        display(self.detect_group)

    def _show_scan_settings(self):
        scan_dwell = widgets.FloatText(value=1.0, description='Dwell Time (us):')
        scan_frame = widgets.IntText(value=1024, description='Frame Size:')
        scan_exptime = widgets.FloatText(value=0.0, description='Exposure Time (s):')
        self.scan_group = widgets.HBox([scan_dwell, scan_frame, scan_exptime])

        acquire_dwell = widgets.FloatText(value=2.0, description='Dwell Time (us):')
        acquire_frame = widgets.IntText(value=1024, description='Frame Size:')
        acquire_exptime = widgets.FloatText(value=0.0, description='Exposure Time (s):')
        self.acquire_group = widgets.HBox([acquire_dwell, acquire_frame, acquire_exptime])
        display(self.scan_group)

    def _show_window_settings(self):
        magnification_select = widgets.IntSlider(value = int(self.microscope.get_magnification_index()),
                                min=0,
                                max=len(self.microscope.magnification_options)-1,
                                description='Magnification:')
        isblanked_select = widgets.Checkbox(value=self.microscope.isblank, description='Blank Beam')
        self.control_group = widgets.HBox([magnification_select, isblanked_select])
        display(self.control_group)

    def show(self):
        self._show_detectors()
        self._show_scan_settings()
        self._show_window_settings()
    
        imaging_button = widgets.Button(description='Update Imaging Settings')
        imaging_button.on_click(self._on_ready)

    def _on_ready(self, b):
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
        _dict['magnification'] = self.microscope.magnification_options[self.control_group.children[0].value]
        _dict['isblanked'] = self.control_group.children[1].value
        self.setup_imaging_settings(**_dict)
    
    def setup_imaging_settings(self, **kwargs): 
            kwargs['scan_exptime'] = kwargs.get('scan_exptime', kwargs['scan_dwell'] * kwargs['scan_frame']**2)
            kwargs['acquire_exptime'] = kwargs.get('acquire_exptime', kwargs['acquire_dwell'] * kwargs['acquire_frame']**2)
            self.microscope._set_imaging_settings(**kwargs) 
            self.state = MicroscopeState.Ready
            self.show()









    


