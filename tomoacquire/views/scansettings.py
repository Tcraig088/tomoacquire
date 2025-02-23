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

class ScanView():
    def __init__(self, controller):
        self.controller = controller
        self.show()

    def show(self):
        scan_detector_dropdown = widgets.SelectMultiple(options = self.controller.microscope.detector_options, description='Scan Detectors:')
        acquire_detector_dropdown = widgets.SelectMultiple(options = self.controller.microscope.detector_options, description='Acquire Detectors:')

        scan_dwell = widgets.FloatText(value=1.0, description='Dwell Time (us):')
        scan_frame = widgets.IntText(value=1024, description='Frame Size:')
        scan_exptime = widgets.FloatText(value=0.0, description='Exposure Time (s):')

        acquire_dwell = widgets.FloatText(value=2.0, description='Dwell Time (us):')
        acquire_frame = widgets.IntText(value=1024, description='Frame Size:')
        acquire_exptime = widgets.FloatText(value=0.0, description='Exposure Time (s):')

        imaging_button = widgets.Button(description='Update Imaging Settings')
        self.detect_group = widgets.HBox([scan_detector_dropdown, acquire_detector_dropdown])
        self.scan_group = widgets.HBox([scan_dwell, scan_frame, scan_exptime])
        self.acquire_group = widgets.HBox([acquire_dwell, acquire_frame, acquire_exptime])
        self.imaging_group = widgets.VBox([imaging_button])

        self.group = widgets.VBox([self.detect_group, self.scan_group, self.acquire_group, self.imaging_group])
        display(self.group)
        imaging_button.on_click(self._on_imaging)

    def _on_imaging(self, b):
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

        if self.controller.state == MicroscopeState.CONNECTED:
            self.controller.update_imaging_settings(**_dict) 
            self.controller.start_imaging()
        elif self.controller.state == MicroscopeState.READY:
            self.controller.stop_imaging()  
            self.controller.update_imaging_settings(**_dict)
            self.controller.start_imaging()
        
        self.group.close()


    

    
        

 


