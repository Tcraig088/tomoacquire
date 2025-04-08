from tomobase.tiltschemes.tiltscheme import TiltScheme
from tomoacquire.controllers.calibrations.base import Calibration

from time import time


@tomoacquire_hook_experiment(name="Tomography")
class TomographyExperiment():
    def __init__():
        pass 

    def setup(self, 
              tiltscheme:TiltScheme=TiltScheme.GRS(-70, 70, 0),
              calibration_method:Calibration=Calibration(), 
              backlash_correct:bool = False):
        
        self.tiltscheme = tiltscheme
        self.calibration = calibration_method
        self.backlash_correct = backlash_correct

    def add_microscope(self, microscope):
        self.microscope = microscope

    def settings(self, use_prediction:bool = False, 
):


        


    