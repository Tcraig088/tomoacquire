import numpy as np
import logging
from . import logs

class PositionCalibrator(logs.Log):
    def __init__(self):  
        self.pid = 0
        self.origin = {}
        self.particle ={}
    def newposition(self):
        if self.pid == 0:
            self.origin['x'] = 1000*(np.random.rand()-0.5)*(10**-6) # 500 to -500 um in m
            self.origin['y'] = 1000*(np.random.rand()-0.5)*(10**-6) # 500 to -500 um in m
            self.origin['z'] = 200*(np.random.rand()-0.5)*(10**-6) # 100 to -100 um in m
            self.cf = 3*(np.random.rand()-0.5)**10-6 # Need to adjust scale
            
            self.particle['x'] = self.origin['x']+self.gettolerance(True)
            self.particle['y'] = self.origin['y']+self.gettolerance(True)
            self.particle['z'] = self.origin['z'] + self.gettolerance(True)
            
        
            
    # set the positional error of how far off axis the alignment is.     
    def gettolerance(self,isx):
        if isx:
            tolerance = 10
        else:
            tolerance = 10
        return tolerance*(np.random.rand()-0.5)*(10**-6)
        
class Projection(logs.Log):
    def __init__(self):
        super().__init__()
        self.Defocus = 1
    
class StemAcqParams(logs.Log):
    def __init__(self):
        self.DwellTime = 1
        self.Binning = 1

class Stage(logs.Log):  
    def __init__(self):
        super().__init__()
        self.Position={
            'x':0,
            'y':0,
            'z':0,
            'a':0,
            'b':0
        }
        pass
    
    def GoTo(self,x=None,y=None, z=None, a=None, b=None):
        np.degrees(a)
        pos = {
            'x':x,
            'y':y,
            'z':z,
            'a':a,
            'b':b
        }
        self.Position = {k: self._check_none(v, self.Position[k]) for k, v in pos.items()}
        if x is not None:
            print(x,y)
                   
    def _check_none(self, new, old):
        if new is None:
            return old
        else:
            return new

class Image:
    def __init__(self):
        self.Name = 'HAADF'
        self.Array = np.random.rand(2048,2048)
                   
class Acquisition(logs.Log):
    def __init__(self):
        super().__init__()
        self.StemAcqParams = StemAcqParams()
        
    def AcquireImages(self):
        size = int(2048/self.StemAcqParams.Binning)
        image = np.random.rand(size,size)
        img = Image()
        img.Array = image
        
        return img



        
class Dummy(logs.Log):
    def __init__(self):
        super().__init__()
        self.Stage = Stage()
        self.Acquisition = Acquisition()
        self.Projection = Projection()
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug('Initialized Dummy Microscope')

    
    
    
    
    
    
    
        