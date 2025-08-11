from threading import Thread, Lock
import time
from tomoacquire.hooks import device_hook
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
from tomobase.log import logger


class FEIMicroscope(QObject):
    scanwindow_updated = Signal()
    acqwindow_updated = Signal()

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
        self._magnification = self.microscope.get_stem_magnification()

    @property
    def magnification(self):
        #self.queue_thread(self.microscope.get_stem_magnification)
        return self._magnification
    
    @magnification.setter
    def magnification(self, value):
        if isinstance(value, int):
            value = self.magnification_options[value]
        logger.info("Setting magnification to %s", value)
        self.queue_thread(self.microscope.set_stem_magnification, value)


    def setmagnification(self, mag):
        if isinstance(mag, int):
            mag = self.magnification_options[mag]
            self.microscope.set_stem_magnification(mag)
    @property
    def isblank(self):
        return self._isblank
    
    @isblank.setter
    def isblank(self, value):
        self.queue_thread(self.blankbeam, value)

    def blankbeam(self, blank):
        self._isblank = blank
        self.microscope.set_beam_blanked(blank)

    def queue_thread(self, func, *args, **kwargs):
        if self.state == ImagingState.Idle:
            self.state = ImagingState.Queued
            acquire_thread = Thread(target=self.exec_thread, args=(func, *args), kwargs=kwargs)
            acquire_thread.daemon = True
            acquire_thread.start()

        else:
            logger.info("cannot queue more than 1 command please wait for execution")

    def exec_thread(self, func, *args, **kwargs):
        while self.state == ImagingState.Queued or self.state == ImagingState.Idle:
            time.sleep(0.05)
        
        func(*args, **kwargs)
        self.state = ImagingState.Idle
        if self._isscaninit:
            self.start_scan()


    def set_scan_mode(self, scanning=True):
        self.queue_thread(self.setscanmode, scanning)

    def set_magnification(self, mag):
        if isinstance(mag, int):
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
        if not self._isscaninit:
            data = np.zeros((len(self._scan_detectors), self._scan_frame, self._scan_frame))
            self.scanwindow = Image(data, pixelsize=1.0)
            self.setscanmode(scanning=True)
            self._isscaninit = True

            data = np.zeros((len(self._acquire_detectors), self._acquire_frame, self._acquire_frame))
            self.acqwindow = Image(data, pixelsize=1.0)


        acquire_thread = Thread(target=self.scan)
        acquire_thread.daemon = True
        acquire_thread.start()

    def update_scanwindow(self, new_data):
        # Convert dictionary to numpy array
        for i, (key, value) in enumerate(new_data.items()):
            self.scanwindow.data[i,:,:] = value
        self.scanwindow_updated.emit() 

    def update_acqwindow(self, new_data):
        # Convert dictionary to numpy array
        for i, (key, value) in enumerate(new_data.items()):
            self.acqwindow.data[i,:,:] = value
        self.acqwindow_updated.emit()


    def scan(self):
        scanning = True
        logger.info("Starting acquisition...")
        while scanning:
            #with self._microscope_lock:  # Ensure thread-safe access
            _dict = self.microscope.acquire(*self.detectors)
            logger.info("Current State: %s", self.state)
            time.sleep(self.sleep)

            if self._isnull:
                for i, item in enumerate(self.detectors):
                    _dict[item] = np.random.random([512, 512])

            if self._isscan:
                self.update_scanwindow(_dict)
                logger.info("Scan window updated")
            else:
                self.update_acqwindow(_dict)
                logger.info("Acquisition window updated")
            
            if self.state == ImagingState.Queued:
                scanning = False

        self.state = ImagingState.Executing
        logger.info("Acquisition complete")









