import enum
import tomobase 

tomobase._datatypes._add_datatype('SCANWINDOW')

class ScanWindow(tomobase.ImageData):
    def __init__(self, data, pixelsize=1.0):
        super().__init__(data, pixelsize)

        self.dosage = 0.0
        self.images_acquired = 0
        self.angle = 0.0
        self.magnification = 1.0
        self.time_start = 0.0
        self.time_current = 0.0
        
