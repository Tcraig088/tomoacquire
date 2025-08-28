

class Base:
    def __init__(self):
        self.detectors ={}
        self.acquisition_frame_size = 1024
        self.acquisition_dwell_time = 4.0
        self.scanning_frame_size = 1024
        self.scanning_dwell_time = 4.0
        self.usescanning = False
        self.dummy =False
        pass
    
    def set(self, view):
        self.detectors = {}
        signals = {
            'BF': 'Analog1',
            'DF4': 'Analog2',
            'HAADF': 'Analog3',
            'DF2': 'Analog4'
            }

        if view.Detectors.BF_var.get():
            self.detectors['BF']=signals['BF']
        if view.Detectors.DF4_var.get():
            self.detectors['DF4']=signals['DF4']
        if view.Detectors.HAADF_var.get():
            self.detectors['HAADF']=signals['HAADF']
        if view.Detectors.DF2_var.get():
            self.detectors['DF2']=signals['DF2']
         
        self.usescanning = view.Imaging.checkbox_var.get()
        self.acquisition_frame_size = int(view.Imaging.AcquisitionParametersWidget.FrameComboBox.get())
        self.acquisition_dwell_time = float(view.Imaging.AcquisitionParametersWidget.DwellSpinBox.get())
        if not self.usescanning:
            self.scanning_frame_size = int(view.Imaging.ScanningParametersWidget.FrameComboBox.get())
            self.scanning_dwell_time = float(view.Imaging.ScanningParametersWidget.DwellSpinBox.get())
        else:
            self.scanning_frame_size = int(view.Imaging.AcquisitionParametersWidget.FrameComboBox.get())
            self.scanning_dwell_time = float(view.Imaging.AcquisitionParametersWidget.DwellSpinBox.get())
        
        self.dummy = view.Submitter.dummy_var.get()
        
    def to_dict(self):
        mydict = {
            'acquisition_frame_size': self.acquisition_frame_size,
            'acquisition_dwell_time': self.acquisition_dwell_time,
            'scanning_frame_size': self.scanning_frame_size,
            'scanning_dwell_time': self.scanning_dwell_time,
            'debug mode': self.dummy
        }
        for k,v in self.detectors.items():
            mydict[k] = k
            
        return mydict