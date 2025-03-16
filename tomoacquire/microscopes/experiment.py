
import enum
import time
import pandas as pd
from tomobase.log import logger

class ExperimentType(enum.Enum):
    NoExperiment = 0
    Tomography = 1
    Calibration = 2

class ExperimentController():
    def __init__(self, microscope, callibration_method=None):
        self._experiment_type = ExperimentType.NoExperiment
        self.callibration_method = None
        self.positions = pd.DataFrame(columns=['particle', 'x', 'y', 'defocus'])
        self._particle_index = 0
        self._magnifications = []
        self.times = {} 

    def start(self, istomo, tiltscheme):
        if istomo:
            self.experiment_type = ExperimentType.Tomography
        else:
            self.experiment_type = ExperimentType.Calibration
        self.tiltscheme = tiltscheme


    def stop(self):
        self.experiment_type = ExperimentType.NoExperiment
        self.reset_positions()
        self.times = {}

        
             
    @property
    def particle_index(self):
        return self._particle_index
    
    @particle_index.setter
    def particle_index(self, particle_index):
        self._particle_index = particle_index
        
    @property
    def experiment_type(self):
        return self._experiment_type
    
    @experiment_type.setter
    def experiment_type(self, experiment_type):
        if self._experiment_type == experiment_type:
            logger.warning(f'Already in state {experiment_type}. Cannot Change Experimental State.')
        else:
            self._experiment_type = experiment_type
            
    def add_position(self):
        df_row = pd.DataFrame({
            'particle': self.particle_index,
            'x': self.microscope.position[0],
            'y': self.microscope.position[1],
            'defocus': self.microscope.defocus
        })
        
        self.positions = pd.concat([self.positions, df_row])    
    
    def reset_positions(self):
        self.positions = pd.DataFrame(columns=['particle', 'x', 'y', 'defocus'])
        self._particle_index = 0
        

        