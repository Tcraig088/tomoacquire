import enum
import tomobase 
from tomobase import TOMOBASE_DATATYPES
import stackview


class ScanWindow(tomobase.data.Image):
    def __init__(self, data, pixelsize=1.0):
        super().__init__(data, pixelsize)

        self.dosage = 0.0
        self.images_acquired = 0
        self.angle = 0.0
        self.magnification = 1.0

    def show(self):
        pass


