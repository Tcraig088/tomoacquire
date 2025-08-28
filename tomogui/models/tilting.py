import tkinter as tk
import enum
import math
import numpy as np

class Binary():
    def __init__(self, angle_min, angle_max, k=8, isbidirectional=True):
        super().__init__()
        self.angle_max = angle_max
        self.angle_min = angle_min
        self.k = k
        
        #Setting parameters
        self.isbidirectional = isbidirectional
        if isbidirectional:
            self.isforward=True
        
        self.step = (self.angle_max - self.angle_min)/(k+0.5)
        self.i = 0
        self.offset = 0
        self.offset_set = 2
        self.offset_run = 1/self.offset_set
        self.angle = 0
        self.max_cutoff = self.angle_max - (self.step/2)
        
        print(self.angle_min, self.angle_max, self.k, self.step)
        
    def get_angle(self,i):
        
        if self.isbidirectional:
            return self._get_angle_bidirectional(i)
        else:
            return self._get_angle_unidirectional() 
    
    def _get_angle_bidirectional(self,i):
        if self.i == i:
            if self.i == 0:
                self.angle = self.angle_min
            return np.round(self.angle,2)
        else: 
            self.i = i
            
        if i == 0:
            self.angle = self.angle_min
        elif self.isforward:
            if np.isclose(self.angle + self.step, self.angle_max) or (self.angle+self.step) > self.angle_max:
                self._get_offsets()
                self.isforward = False
                if np.isclose(self.max_cutoff + (self.step*self.offset), self.angle_max) or (self.max_cutoff + (self.step*self.offset)) >=  self.angle_max:
                    self.angle = self.max_cutoff + (self.step*self.offset) - self.step
                else:
                    self.angle = self.max_cutoff + (self.step*self.offset)
                self.step *= -1 
            else:
                self.angle = self.angle + self.step
        else:
            if np.isclose(self.angle+self.step, self.angle_max) or (self.angle+self.step) < self.angle_min:
                self._get_offsets()
                self.isforward = True
                self.angle = self.angle_min + (np.abs(self.step)*self.offset)
                self.step *= -1
            else:
                self.angle = self.angle + self.step
        i += 1
        print(self.angle)
        return np.round(self.angle,2)
    
    
    def _get_angle_unidirectional(self):
        if self.i == 0:
            self.angle = self.angle_min
        elif np.isclose(self.angle + self.step, self.angle_max) or (self.angle + self.step) > self.angle_max:
            self._get_offsets()
            self.angle = self.angle_min + (self.step * self.offset)
        else:
            self.angle += self.step
        self.i += 1
        return np.round(self.angle, 2)
    
    def _get_offsets(self):
        if (self.offset + 0.5) >= 1:
            if self.offset == ((self.offset_set-1)/(self.offset_set)):
                self.offset_set = self.offset_set*2
                self.offset_run = 1/self.offset_set
                self.offset = self.offset_run
            else:
                self.offset_run += 2/self.offset_set
                self.offset = self.offset_run
        else:
            self.offset += 0.5  
            
    def get_angle_array(self, indices):
        return super().get_angle_array(indices)
        
    def isfinished(self, angle):
        return False 
        
class GRS():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.gr = (math.sqrt(5)+1)/2
        self.alpha = np.radians(end-start)
    def get_angle(self,i):
        angle = np.degrees((i*self.gr*self.alpha)%self.alpha)+self.start
        print(angle)
        return angle
        
    def isfinished(self,angle):
        return False
    
class Incremental():
    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step
    def get_angle(self,i):
        return self.start + i*self.step
    
    def isfinished(self, angle):
        if angle > self.end:
            return True
        else:
            return False
    
class TiltScheme(enum.Enum):
    GRS = 1
    Incremental = 2
    Binary = 3

class TrackingScheme:
    def __init__(self):
        pass
    

class Base:
    def __init__(self):
        self.file = ''
        self.tiltscheme_select = TiltScheme.GRS
        self.tiltscheme = GRS(-70,70)
        self.fasttomo = False
        self.usemanual = False
        self.backlashcorrect = True 
        self.comcorrect = False
        self.hightiltangle = 50
        self.hightiltpause = 1.0
        self.pause = 1.0
        
    def set(self, view):
        tiltscheme_select = TiltScheme[view.Settings.selected_option.get()]
        if tiltscheme_select == TiltScheme.GRS:
            self.tiltscheme = GRS(float(view.TiltScheme.GRSWidget.StartSpinBox.get()), float(view.TiltScheme.GRSWidget.EndSpinBox.get()))
        elif tiltscheme_select == TiltScheme.Incremental:
            self.tiltscheme = Incremental(float(view.TiltScheme.IncrementalWidget.StartSpinBox.get()), float(view.TiltScheme.IncrementalWidget.EndSpinBox.get()), float(view.TiltScheme.IncrementalWidget.StepSpinBox.get()))
        elif tiltscheme_select == TiltScheme.Binary: 
            self.tiltscheme = Binary(float(view.TiltScheme.BDWidget.StartSpinBox.get()), float(view.TiltScheme.BDWidget.EndSpinBox.get()), float(view.TiltScheme.BDWidget.KSpinBox.get()))
        else:
            raise ValueError('Tilt Scheme not supported')
        
        self.file = view.Settings.FileEntryWidget.FileEntry.get()
        self.fasttomo = view.AdvancedSettings.fasttomo_var.get()
        self.usemanual = view.AdvancedSettings.usemanual_var.get()
        self.backlashcorrect = view.AdvancedSettings.backlashcorrect_var.get()
        self.comcorrect = view.AdvancedSettings.comcorrect_var.get()
        self.hightiltangle = float(view.AdvancedSettings.FasttomoWidget.HighTiltSpinBox.get())
        self.hightiltpause = float(view.AdvancedSettings.FasttomoWidget.HighTiltPauseSpinBox.get())
        self.pause = float(view.AdvancedSettings.FasttomoWidget.PauseSpinBox.get())
        
    def to_dict(self):
        mydict =  {'tiltscheme': self.tiltscheme_select.name,
                'usemanual': self.usemanual,
                'backlashcorrect': self.backlashcorrect,
                'comcorrect': self.comcorrect,
                'fasttomo': self.fasttomo
                }
        if self.fasttomo:
            mydict['hightiltangle'] = self.hightiltangle
            mydict['hightiltpause'] = self.hightiltpause
            mydict['pause'] = self.pause
            
        return mydict