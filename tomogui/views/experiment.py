import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Summary(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Summary', padx=10, pady=10)
        self.pack(fill=tk.X)
        
        self.ImagesLabel = tk.Label(self, text='Images Acquired:')
        
        self.images_val = tk.IntVar()
        self.images_val.set(0)
        self. ImagesSpinBox = tk.Spinbox(self, from_=0, to=10000, state='readonly', textvariable = self.images_val)
        
        self.angles_val = tk.DoubleVar()
        self.angles_val.set(0)
        self.CurrentAngleLabel = tk.Label(self, text='Current Angle:')
        self.CurrentAngleSpinBox = tk.Spinbox(self, from_=-90.0, to=90.0, state='readonly', textvariable=self.angles_val)
        
        
        self.Dosage = tk.Label(self, text='Accumulated Dosage:')
        self.CurrentAngleSpinBox = tk.Spinbox(self, from_=0, to=10000, state='readonly', textvariable=self.angles_val)
        
        self.ImagesLabel.grid(row=0, column=0, sticky=tk.W)
        self.ImagesSpinBox.grid(row=0, column=1, sticky=tk.W)
        self.CurrentAngleLabel.grid(row=1, column=0, sticky=tk.W)
        self.CurrentAngleSpinBox.grid(row=1, column=1, sticky=tk.W)
        self.CurrentAngleLabel.grid(row=2, column=0, sticky=tk.W)
        self.CurrentAngleSpinBox.grid(row=2, column=1, sticky=tk.W)
        self.pack()

class Submitter(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Run Experiment', padx=10, pady=10)
        padx=2
        
        self.scanning_state = False
        self.SubmitButton = tk.Button(self, text='Start')
        self.NextAngleButton = tk.Button(self, text='Next Angle')
        
        self.SubmitButton.pack(padx =padx, anchor=tk.W, side=tk.LEFT)
        self.NextAngleButton.pack(padx=padx, anchor=tk.W, side=tk.LEFT)

        self.pack(fill=tk.X)
        
        self.NextAngleButton.pack_forget()

class BaseFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Summary = Summary(self)
        self.Submitter = Submitter(self)
        
        self.Summary.pack(fill=tk.X)
        self.Submitter.pack(fill=tk.X)
        self.pack(fill=tk.X)