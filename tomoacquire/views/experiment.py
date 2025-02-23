import time
import enum
from ipywidgets import widgets
from IPython.display import display
from threading import Thread
from tomobase.log import logger
from tomoacquire.scanwindow import ScanWindow
from tomoacquire import config as mc
from threading import Thread
import numpy as np
import stackview
from tomobase.registrations.tiltschemes import TOMOBASE_TILTSCHEMES
from tomoacquire.states import MicroscopeState, ImagingState

class ExperimentView():
    def __init__(self, controller):
        self.controller = controller

    def show_adjust_settings(self):
        tiltscheme_select = widgets.Dropdown(options = TOMOBASE_TILTSCHEMES, description='Tilt Scheme:')
        tracking_select = widgets.Dropdown(options = ['None', 'Mastranade'], description='Tracking:')
    
        interem_tiltstep = widgets.FloatText(value=90, description='Interem Tilt Step:')
        magnifications = widgets.SelectMultiple(options = self.controller.microscope.magnification_options, description='Magnifications:')
    
    
    def show_experiment(self):
        use_automoation = widgets.Checkbox(value=False, description='Use Automation')
        use_predictions = widgets.Checkbox(value=False, description='Use Predictions')
        blank_beam_checkbox = widgets.Checkbox(value=False, description='Blank Beam')
        current_magnification = widgets.IntSlider(value=0, min=0, max=10, description='Magnification')




    

    
        

 


