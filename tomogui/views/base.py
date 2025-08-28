import logging
import tkinter as tk
from tkinter import ttk
from . import imaging, calibration, logger, tilting, experiment
         
class View(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Tomography Acquisition Gui")
        self.notebook = ttk.Notebook(self)

        self.ImagingTab = ttk.Frame(self.notebook)
        self.CallibrationTab = ttk.Frame(self.notebook)
        self.TomographyTab = ttk.Frame(self.notebook)
        self.ExperimentTab = ttk.Frame(self.notebook)
        self.LoggingTab = ttk.Frame(self.notebook)

        self.notebook.add(self.ImagingTab, text='Imaging')
        self.notebook.add(self.CallibrationTab, text='Callibration')
        self.notebook.add(self.TomographyTab, text='Tomography')
        self.notebook.add(self.ExperimentTab, text='Experiment')
        self.notebook.add(self.LoggingTab,text ='Logs')
        self.ImagingFrame =  imaging.BaseFrame(self.ImagingTab)
        self.CalibrationFrame = calibration.BaseFrame(self.CallibrationTab)
        self.TomographyFrame = tilting.BaseFrame(self.TomographyTab)
        self.ExperimentFrame = experiment.BaseFrame(self.ExperimentTab) 
        self.LoggingFrame =  logger.BaseFrame(self.LoggingTab)
        
        self.notebook.pack(padx=10, pady=10)
        log = logging.getLogger('TKLogger')
        log.info("Start up")
        
        #self.Logger.pack(padx=10, pady=10, side=tk.RIGHT)
