"""
@tomoacquire_hook(name="FEIP")
class FEIMicroscope_old(QObject):
    scanwindow_updated = Signal()

    def __init__(self, address, port, magnifications, detectors, detector_pixelsize):
        super().__init__()
        self.detector_options = detectors
        self.magnification_options = np.array(magnifications)
        self.detector_pixelsize = detector_pixelsize
        
        self._isnull = False
        self.address = address
        self.port = port
        self._initialize_microscope()

    def _initialize_microscope(self):
        if self.address == 'localhost':
            if self.port == 0:
                self.microscope = self._import_temscript().NullMicroscope()
                self._isnull = True
            else:
                self.microscope = self._import_temscript().Microscope()
        else:
            self.microscope = self._import_temscript().RemoteMicroscope((self.address, str(self.port)))

    def _import_temscript(self):
        import temscript
        return temscript

    def _set_imaging_settings(self, **kwargs):
        for key, value in kwargs.items():
            match key:
                case 'scan_detectors':
                    self._scan_detectors = value
                case 'scan_dwell':
                    self._scan_dwell = value
                case 'scan_frame':
                    self._scan_frame = value
                case 'scan_exptime':
                    self._scan_exptime = value
                case 'dwell_detectors':
                    self._acquire_detectors = value
                case 'acquire_dwell':
                    self._acquire_dwell = value
                case 'acquire_frame':
                    self._acquire_frame = value
                case 'acquire_exptime':
                    self._acquire_exptime = value

    def start_imaging(self):
        new_thread = Thread(target=self.acquire)
        new_thread.daemon = True
        new_thread.start()
        self.imaging_thread_open = True

    def stop_imaging(self):
        self.is_imaging = False
        self.imaging_thread_open = False

    def acquire(self):
        pythoncom.CoInitialize()  # Initialize COM in the correct threading mode
        while self.is_imaging:
            _dict = self.microscope.acquire(*self.detectors)
            if self._isnull:
                for i, item in enumerate(self.detectors):
                    _dict[item] = np.random.random([512, 512])
            time.sleep(self.sleep)
            if self._isscan:
                self.update_scanwindow(_dict)
        pythoncom.CoUninitialize()  # Uninitialize COM when done

    def update_scanwindow(self, new_data):
        # Convert dictionary to numpy array
        for i, (key, value) in enumerate(new_data.items()):
            new_data[i,:,:] = value
        self.scanwindow.data = new_data
        self.scanwindow_updated.emit()

@tomoacquire_hook(name="FEI2")
class FEIMicroscope_old2(QObject):
    scanwindow_updated = Signal()

    def __init__(self, address, port, magnifications, detectors, detector_pixelsize):
        super().__init__()
        self._isready = False
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
        self._initialize_microscope()

    def _initialize_microscope(self):
        if self.address == 'localhost':
            if self.port == 0:
                self.microscope = self._import_temscript().NullMicroscope()
                self._isnull = True
            else:
                self.microscope = self._import_temscript().Microscope()
        else:
            self.microscope = self._import_temscript().RemoteMicroscope((self.address, str(self.port)))

    def _import_temscript(self):
        import temscript
        return temscript

    @property
    def isblank(self):
        print('reading isblank')    
        return self.microscope.get_beam_blanked()
    
    @isblank.setter
    def isblank(self, value):
        self._isblank = value
        print('setting isblank')
        self.microscope.set_beam_blanked(value)

    @property
    def isnull(self):
        return self._isnull 

    @property
    def isready(self):
        return self._isready
    
    @isready.setter
    def isready(self, value):
        self._isready = value

    @property
    def isscan(self):
        return self._isscan
    
    @isscan.setter
    def isscan(self, value):
        self._isscan = value
        if self.isscan:
            self.sleep = self._scan_exptime
            self.detectors = self._scan_detectors
            _dict = {"image_size": "FULL",
                     "dwell_time(s)": self._scan_dwell    }
            if not self.isnull:
                _dict["binning"] = 2048/self._scan_frame
        else:
            self._sleep = self._acquire_exptime
            self.detectors = self._acquire_detectors
            _dict = {"image_size": "FULL",
                     "dwell_time(s)": self._acquire_dwell    }
            if not self.isnull:
                _dict["binning"] = 2048/self._acquire_frame
        self.microscope.set_stem_acquisition_param(_dict)

    @property
    def magnification(self):
        return self.microscope.get_stem_magnification()
    
    @magnification.setter
    def magnification(self, mag):
        if type(mag) == int:
            mag = self.magnification_options[mag]
        self.microscope.set_stem_magnification(mag) 
    
    def get_magnification_index(self):
        magnification = self.magnification
        index = np.argmin(np.abs(self.magnification_options - magnification))
        return index

    def _set_imaging_settings(self, **kwargs):
        for key, value in kwargs.items():
            match key:
                case 'scan_detectors':
                    self._scan_detectors = value
                case 'scan_dwell':
                    self._scan_dwell = value
                case 'scan_frame':
                    self._scan_frame = value
                case 'scan_exptime':
                    self._scan_exptime = value
                case 'dwell_detectors':
                    self._acquire_detectors = value
                case 'acquire_dwell':
                    self._acquire_dwell = value
                case 'acquire_frame':
                    self._acquire_frame = value
                case 'acquire_exptime':
                    self._acquire_exptime = value
                case 'magnification':
                    self.magnification = value
                case 'isblanked':
                    self.isblanked = value

        #acq_data = np.zeros((self._acquire_frame, self._acquire_frame, len(self._scan_detectors)))
        scan_data = np.zeros((self._scan_frame, self._scan_frame, len(self._acquire_detectors)))
        self.image = Image(scan_data)
        #self.sinogram = Sinogram(acq_data, np.array([0]*len(self._acquire_detectors)))

        if not self.isready:
            self.isscan = True
            while not self.isscan:
                pass
            self.isready = True
            acquire_thread = Thread(target=self.acquire)
            acquire_thread.daemon = True
            acquire_thread.start()

    def acquire(self):
        pythoncom.CoInitialize()  # Initialize COM in the correct threading mode
        while self.isready:
            print(self.state)
            if self.state == ImagingState.Idle:
                self.state = ImagingState.Blocked
                _dict = self.microscope.acquire(*self.detectors)
                if self.isnull:
                    for i, item in enumerate(self.detectors):
                        _dict[item] = np.random.random(self.image.data.shape)[i,:,:].squeeze()
                time.sleep(self.sleep)
                if self.isscan:
                    print("Updating image")
                    if len(self.detectors) == 1:
                        self.image.data[0,:,:] = _dict[self.detectors[0]]
                        self.image.view.update()
                    else:
                        for i, (key, value) in enumerate(_dict.items()):
                            self.image[i,:,:] = value
                else:
                    for i, (key, value) in enumerate(_dict.items()):
                        if key in self.detectors:
                            self.sinogram[i,:,:] = value
                
                if self.state == ImagingState.Blocked:
                    self.state = ImagingState.Idle
                elif self.state == ImagingState.Requested:
                    self.state = ImagingState.Queued
            else:
                time.sleep(0.1)
        pythoncom.CoUninitialize()  # Uninitialize COM when done
"""