from tomoacquire.hooks import tomoacquire_hook
import temscript
import numpy as np 
import stackview
from IPython.display import display
from ipywidgets import widgets


@tomoacquire_hook(name="FEI")
class FEIMicroscope():
    def __init__(self, address, port, magnifications):
        self._mag_list = np.array(magnifications)
        self.magnifications_total = len(self._mag_list)
        self.detectors = ['HAADF', 'DF2', 'DF4', 'BF']
        
        self._scan_dwell = 0.1
        self._scan_frame = 1
        self._scan_exptime = 0.1

        self._acquire_dwell = 0.1
        self._acquire_frame = 1
        self._acquire_exptime = 0.1

        self._isscan = False
        self._scan_window = None
        self.acq_window = None

        if address == 'localhost':
            self.microscope = temscript.Microscope()
        else:
            print(address, port)
            print(type(address), type(port))
            self.microscope = temscript.RemoteMicroscope((address, str(port)))

    @property
    def isscan(self):
        return self._isscan
    
    @isscan.setter
    def isscan(self, value):
        self._isscan = value
        if self.isscan:
            self.sleep = self._scan_exptime
            _dict = {"image_size": "FULL",
                     "binning": 2048/self._scan_frame,
                     "dwell_time(s)": self._scan_dwell	}
        else:
            self._sleep = self._acquire_exptime
            _dict = {"image_size": "FULL",
                     "binning": 2048/self._acquire_frame,
                     "dwell_time(s)": self._acquire_dwell	}
        print('image_timings',_dict)
        self.microscope.set_stem_acquisition_param(_dict)

    @property
    def magnification(self):
        return self.microscope.get_stem_magnification()
    
    @magnification.setter
    def magnification(self, mag):
        if type(mag) == int:
            mag = self._mag_list[mag]
        self.microscope.set_stem_magnification(mag) 
    
    def get_magnification_index(self):
        #find index in maglist closests to actual magnification
        magnification = self.magnification
        index = np.argmin(np.abs(self._mag_list - magnification))
        return index

    def get_detectors(self):
        return self.detectors
    
    def imaging_settings(self, detectors, scan_dwell, scan_frame, scan_exptime, acquire_dwell, acquire_frame, acquire_exptime):
        print('set imaging mode')
        self.detectors_active = detectors
        self._scan_dwell = scan_dwell
        self._scan_frame = scan_frame
        self._scan_exptime = scan_exptime
        self._acquire_dwell = acquire_dwell
        self._acquire_frame = acquire_frame
        self._acquire_exptime = acquire_exptime

        self._scan_window = np.zeros((len(self.detectors_active),self._scan_frame, self._scan_frame))
        self._acq_window = np.zeros((len(self.detectors_active),self._acquire_frame, self._acquire_frame))
        print(self._scan_window.shape, self._acq_window.shape)  
        self.show_scan()

    
    def acquire(self):
        print('start acquisition')
        print(self._scan_dwell)
        while True:
            print('_dict')
            _dict = self.microscope.acquire(*self.detectors_active)
            print(_dict)
            if self.isscan:
                #for each entry in the dict enumerated
                for i, (key, value) in enumerate(_dict.items()):
                    if key in self.detectors:
                        self._scan_window[i,:,:] = value
            else:
                for i, (key, value) in enumerate(_dict.items()):
                    if key in self.detectors:
                        self._acq_window[i,:,:] = value

   
    def show_scan(self):
        self.scan = stackview.slice(self._scan_window, continuous_update=True)
        self.acq = stackview.slice(self._acq_window, continuous_update=True)
        display(widgets.HBox([self.scan, self.acq]))
                
            

