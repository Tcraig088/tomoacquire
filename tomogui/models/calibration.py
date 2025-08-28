import pandas as pd

class Axis:
    def __init__(self):
        self.m = 0
        self.c = 0
        self.f = 1

class Calibration:
    def __init__(self):
        self.positions = pd.DataFrame(columns=['id', 'x', 'y', 'f'])
        self.axial_positions = pd.DataFrame(columns=['x', 'y'])
        pass
    
    def estimate_origin(self):
        pass
    
    def estimate_axis(self):
        pass
    
    def adjust_estimate(self):
        pass
    
class Base:
    def __init__(self):
        self.Calibration = Calibration()
        pass