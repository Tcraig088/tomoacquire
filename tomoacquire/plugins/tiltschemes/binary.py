
import numpy as np

from qtpy.QtWidgets import QDoubleSpinBox, QSpinBox, QGridLayout, QLabel

from tomobase.napari.components import CollapsableWidget
from tomoacquire.plugins.tiltschemes.tiltscheme import Tiltscheme
from tomoacquire.plugins.hooks import tomoacquire_hook_tiltscheme


@tomoacquire_hook_tiltscheme('BINARY')
class BinaryWidget(CollapsableWidget):
    def __init__(self, parent=None):
        super().__init__('Binary Decomposition TiltScheme', parent)
        
        self.angle_max = QDoubleSpinBox()
        self.angle_max.setRange(-90, 90)
        self.angle_max.setValue(70)
        
        self.angle_min = QDoubleSpinBox()
        self.angle_min.setRange(-90, 90)
        self.angle_min.setValue(-70)
        
        self.index = QSpinBox()
        self.index.setRange(1, 1000)
        self.index.setValue(1)
        
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Angle Max ('\u00B0')"), 0, 0)
        self.layout.addWidget(self.angle_max, 0, 1)
        self.layout.addWidget(QLabel("Angle Min ('\u00B0')"), 1, 0)
        self.layout.addWidget(self.angle_min, 1, 1)
        self.layout.addWidget(QLabel("Index"), 2, 0)
        self.layout.addWidget(self.index, 2, 1)
        
    def setTiltScheme(self):
        return Binary(self.angle_max.value(), self.angle_min.value(), self.index.value())
    
@tomoacquire_hook_tiltscheme('BINARY')  
class Binary(Tiltscheme):
    def __init__(self, angle_max, angle_min, k=8):
        super().__init__()
        self.angle_max = angle_max
        self.angle_min = angle_min
        self.k = k
        self.M = 1
        self.step = (self.angle_max - self.angle_min)/k
        
    def get_angle(self):
        self.M = self.index//self.k + 1
        step = self.step
        angle = self.angle_min + (self.index*step)
        if angle + step > self.angle_max:
            self.isfinished = True
        self.index += 1
        
        return angle
    
    def get_angle_array(self, indices):
        for i in indices:
            
        
        angles = np.mod(indices*self.gr*self.range, self.range) + np.radians(self.angle_min)
        return np.degrees(angles)