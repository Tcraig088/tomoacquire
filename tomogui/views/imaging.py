import tkinter as tk
from tkinter import ttk

class Submitter(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Confirm Values', padx=10, pady=10)
        padx = 2    
        self.SubmitButton = tk.Button(self, text='Confirm')
        self.SubmitButton.pack(padx=padx, side = tk.LEFT)
        self.dummy_var = tk.IntVar(value=0)
        
        self.DummyCheckBox = tk.Checkbutton(self, text='Use Dummy Microscope (Debug Mode)', variable=self.dummy_var)
        self.DummyCheckBox.pack(padx=padx, side = tk.LEFT)
        self.pack(fill=tk.X)

class Detectors(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Detectors', padx=10, pady=10)
        self.HAADF_var = tk.IntVar(value=1)
        self.HAADFCheckBox = tk.Checkbutton(self, text='HAADF', variable=self.HAADF_var)
        self.DF4_var = tk.IntVar(value=0)
        self.DF4CheckBox = tk.Checkbutton(self, text='DF4', variable=self.DF4_var)
        self.DF2_var = tk.IntVar(value=0)
        self.DF2CheckBox = tk.Checkbutton(self, text='DF2', variable=self.DF2_var)
        self.BF_var = tk.IntVar(value=0)
        self.BFCheckBox = tk.Checkbutton(self, text='BF', variable=self.BF_var)
        
        self.HAADFCheckBox.pack(side = tk.LEFT)
        self.DF4CheckBox.pack(side = tk.LEFT)
        self.DF2CheckBox.pack(side = tk.LEFT)
        self.BFCheckBox.pack(side = tk.LEFT)
        
        self.pack(fill=tk.X)
        
class ImageParams(tk.Frame): 
    def __init__(self, parent):
        super().__init__(parent)
        self.FrameLabel = tk.Label(self, text='Frame Size (px) :')
        self.FrameComboBox = ttk.Combobox(self, values=[256, 512, 1024, 2048])
        self.FrameComboBox.set('1024')
        
        self.DwellLabel = tk.Label(self, text='Dwell Time (us) :')
        self.DwellSpinBox = tk.Spinbox(self, from_=0.1, to=1000, increment=0.5)
        self.DwellSpinBox.delete(0, 'end')
        self.DwellSpinBox.insert(0, '4.0')
        
        self.FrameLabel.pack(side = tk.LEFT)
        self.FrameComboBox.pack(side = tk.LEFT)
        self.DwellLabel.pack(side = tk.LEFT)
        self.DwellSpinBox.pack(side = tk.LEFT)
        
          
class Imaging(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Imaging Settings', padx=10, pady=10)
        self.AqLabel = tk.Label(self, text='Acquisition Settings :')
        self.AcquisitionParametersWidget = ImageParams(self)
        
        self.checkbox_var = tk.IntVar(value=1)  # Create a variable to track the checkbox state
        self.ScanningCheckBox = tk.Checkbutton(self, text='Use Same Search Settings', variable=self.checkbox_var, command=self.toggle_params)
        
        self.ScanningLabel = tk.Label(self, text='Scanning Settings :')
        self.ScanningParametersWidget = ImageParams(self)
        
        self.AqLabel.grid(row=0, column=0, sticky='w')
        self.AcquisitionParametersWidget.grid(row=1, column=0, sticky='w')
        self.ScanningCheckBox.grid(row=2, column=0, sticky='w')
        self.ScanningLabel.grid(row=3, column=0, sticky='w')
        self.ScanningParametersWidget.grid(row=4, column=0, sticky='w')
        
        self.ScanningLabel.grid_remove()
        self.ScanningParametersWidget.grid_remove()
        
        self.pack(fill=tk.X)
        
    def toggle_params(self):
        if not self.checkbox_var.get():  # Use the variable to check the checkbox state
            self.ScanningLabel.grid()
            self.ScanningParametersWidget.grid()
        else:
            self.ScanningLabel.grid_remove()
            self.ScanningParametersWidget.grid_remove()
            
class BaseFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Detectors = Detectors(self)
        self.Imaging = Imaging(self)
        self.Submitter = Submitter(self)
        
        self.Imaging.pack(fill=tk.X)
        self.Detectors.pack(fill=tk.X)
        self.Submitter.pack(fill=tk.X)
        
        self.pack(fill=tk.X)