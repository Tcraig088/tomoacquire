import tkinter as tk
from tkinter import ttk

class Summary(tk.LabelFrame):   
    def __init__(self, parent):
        super().__init__(parent, text='Summary', padx=10, pady=10)
        self.Labels = []
        self.Entries = []
        
        self.Labels.append(tk.Label(self, text='Particle ID:'))
        self.Labels.append(tk.Label(self, text='Angle:'))
        self.Labels.append(tk.Label(self, text='X:'))
        self.Labels.append(tk.Label(self, text='Y:'))
        self.Labels.append(tk.Label(self, text='Defocus:'))
                           
                           
class Submitter(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Callibrate Rotation Axis', padx=10, pady=10)
        padx= 2
        
        self.SubmitButton = tk.Button(self, text='Start')
        self.NextAngleButton = tk.Button(self, text='Next Angle')
        self.NextParticleButton = tk.Button(self, text='Next Particle')
        self.ResetButton = tk.Button(self, text='Reset')
        
        self.SubmitButton.pack(padx=padx, side=tk.LEFT)
        self.ResetButton.pack(padx=padx, side=tk.LEFT)
        self.NextAngleButton.pack(padx=padx, side=tk.LEFT)
        self.NextParticleButton.pack(padx=padx,  side=tk.LEFT)
        
        
        self.pack(fill=tk.X)
        
        self.NextAngleButton.pack_forget()
        self.NextParticleButton.pack_forget()
        
class BaseFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Submitter = Submitter(self)
        
        self.Submitter.pack(fill=tk.X)
        self.pack(fill=tk.X)
