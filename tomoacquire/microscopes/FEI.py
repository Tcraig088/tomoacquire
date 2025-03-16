from tomoacquire.hooks import tomoacquire_hook
from tomobase.data import Sinogram, Image
import numpy as np
from IPython.display import display
from ipywidgets import widgets
from threading import Thread
import time
import enum

import temscript
from tomoacquire.states import ImagingState
from qtpy.QtCore import Signal, QObject
#import pythoncom

@tomoacquire_hook(name="FEI")
class FEIMicroscope(QObject):
    scanwindow_updated = Signal()

    def __init__(self, address, port, magnifications, detectors, detector_pixelsize):
        super().__init__()

        self._isscaninit = False
        self._isscan = False
        self._isnull = False
        self._isblank = False
        self.state = ImagingState.Idle   

        self.detector_options = detectors
        self.magnification_options = np.array(magnifications)
        self.detector_pixelsize = detector_pixelsize

        self._isnull = False
        self.address = address
        self.port = port

        if self.address == 'localhost':
            if self.port == 0:
                self.microscope = temscript.Microscope()
                self._isnull = True
            else:
                self.microscope = temscript.Microscope()
        else:
            self.microscope = temscript.RemoteMicroscope((self.address, str(self.port)))

    @property
    def isblank(self):
        return self._isblank
    
    @isblank.setter
    def isblank(self, value):
        self._isblank = value
        self.microscope.set_beam_blanked(value)

    def set_magnification(self, index):
        if type(mag) == int:
            mag = self.magnification_options[mag]
            self.microscope.set_stem_magnification(mag)

    def set_scan(self, scan_dict):
        self._scan_dwell = scan_dict['dwell']
        self._scan_frame = scan_dict['frame']
        self._scan_exptime = scan_dict['exptime']

    def set_acquisition(self, acquisition_dict):
        self._acquire_dwell = acquisition_dict['dwell']
        self._acquire_frame = acquisition_dict['frame']
        self._acquire_exptime = acquisition_dict['exptime']

    def set_detectors(self, detectors):
        self._scan_detectors = detectors
        self._acquire_detectors = detectors
    
    def setscanmode(self, scanning=True):
        self._isscan = scanning
        if self._isscan:
            self.sleep = self._scan_exptime
            self.detectors = self._scan_detectors
            _dict = {"image_size": "FULL",
                     "dwell_time(s)": self._scan_dwell    }
            if not self._isnull:
                _dict["binning"] = 2048/self._scan_frame
        else:
            self._sleep = self._acquire_exptime
            self.detectors = self._acquire_detectors
            _dict = {"image_size": "FULL",
                     "dwell_time(s)": self._acquire_dwell    }
            if not self._isnull:
                _dict["binning"] = 2048/self._acquire_frame
        self.microscope.set_stem_acquisition_param(_dict)

    def start_scan(self):
        data = np.zeros((len(self._scan_detectors), self._scan_frame, self._scan_frame))
        self.scanwindow = Image(data, pixelsize=1.0)
        self.setscanmode(scanning=True)
        self._isscaninit = True
        
        acquire_thread = Thread(target=self.acquire)
        acquire_thread.daemon = True
        acquire_thread.start()

    def update_scanwindow(self, new_data):
        # Convert dictionary to numpy array
        for i, (key, value) in enumerate(new_data.items()):
            self.scanwindow.data[i,:,:] = value
        self.scanwindow_updated.emit() 

    def acquire(self):
         while self._isscaninit:
            _dict = self.microscope.acquire(*self.detectors)
            if self._isnull:
                for i, item in enumerate(self.detectors):
                    _dict[item] = np.random.random([512, 512])
            time.sleep(self.sleep)
            if self._isscan:
                self.update_scanwindow(_dict)









