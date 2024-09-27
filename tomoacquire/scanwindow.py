import enum
import tomobase 

tomobase._datatypes._add_datatype('SCANWINDOW')

class ScanWindow(tomobase.Data):
    def __init__(self, data, pixelsize=1.0):
        super().__init__(data, pixelsize)
        
