import time

from tomoacquire.controllers.acquisition import AcquireController

class StageController(AcquireController):
    def __init__(self, microscope, scan_time):
        self.microscope = microscope
        self.scan_time = scan_time
        
        self._automate = False
        self._speed = 0.0
        self._pause_long = 0.0
        self._pause_short = 0.0
        self._high_tilt = 90.0
        self._intermediate_tilt = 90.0
        self._intermediate_pause_time = 0.0
        
        self.backlash_corrected = True
        self._useprediction = False
        self._use_interem_tilts = False
        self._use_interem_prediction = False
        self._confidence = 10
        self.isconfident = False

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        
    
    def get_interem(self, angle):
        if self._use_interem_tilts == False:
            return angle
        if angle > self.microscope.angle:
            if (self.microscope.angle + self._intermediate_tilt) < angle:
                return self.microscope.angle + self._intermediate_tilt
            else:
                return 0.0
            
        elif angle < self.microscope.angle:
            if (self.microscope.angle - self._intermediate_tilt) > angle:
                return self.microscope.angle - self._intermediate_tilt
            else:
                return 0.0
            
    def move(self, angle):
        while self.microscope.angle != angle:
            self.microscope.blanked = True
            interem_angle = self.get_interem(angle)
            if interem_angle != 0.0:
                used_angle = interem_angle
            else:
                used_angle = angle

            if self.backlash_corrected:  
                if self.microscope.angle > used_angle:
                    self.microscope.tilt(used_angle - 2)
                    self.microscope.tilt(used_angle)  
                else:
                    self.microscope.tilt(used_angle) 
            
            time.sleep(0.01)       
            if self._useprediction:  
                if (used_angle == angle) or self._use_interem_prediction:
                    x,y,f  = self.algorithm.predict(used_angle)
                    if self.isconfident:
                        self.microscope.position = (x,y)
                        self.microscope.defocus = f
                    
            self.microscope.blanked = False
            time.sleep(self.scan_time)