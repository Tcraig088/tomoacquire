
class AcquisitionController():
    def __init__(self, microscope, detectors):
        
        self.microscope = microscope
        self.microscope.set_detectors(detectors)
        self.detectors = []
        self._isscan = True
        
    @property
    def isscan(self):
        return self._isscan
    
    @isscan.setter
    def isscan(self, isscan):
        self._isscan = isscan
