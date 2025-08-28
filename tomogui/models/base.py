
from . import calibration, tilting, imaging
     
class Model:
    def __init__(self):
        self.tilting = tilting.Base()
        self.imaging = imaging.Base()
        self.callibration = calibration.Base()

    def to_dict(self):
        return {'tilting': self.tilting.to_dict(),
                'imaging': self.imaging.to_dict() }