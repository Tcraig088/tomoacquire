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

from tomoacquire.controllers.base import BaseController

class ExperimentController(BaseController):
    def __init__(self):
        super().__init__()

    def _show_window_settings(self):
        magnification_select = widgets.IntSlider(value = int(self.microscope.get_magnification_index()),
                                min=0,
                                max=len(self.microscope.magnification_options)-1,
                                description='Magnification:')
        isblanked_select = widgets.Checkbox(value=self.microscope.isblank, description='Blank Beam')
        self.control_group = widgets.HBox([magnification_select, isblanked_select])


        magnification_select.observe(s  elf._on_magnification_change, names='value')
        isblanked_select.observe(self._on_blank_change, names='value')

    def _show_experiment_settings(self):
        tiltscheme = widgets.Dropdown(options = TOMOBASE_TILTSCHEMES.keys(), description='Tilt Scheme:')
        tiltscheme_select = widgets.Button(description='Select')
        self.tiltscheme_group = widgets.HBox([tiltscheme, tiltscheme_select])

        experiment = widgets.Dropdown(options = ['Tomography', 'Callibration'], description='Experiment:')
        magnification_select = widgets.SelectMultiple(options = self.microscope.magnification_options, description='Magnifications:')
        self.experiment_type_group = widgets.HBox([experiment, self.tiltscheme_group, magnification_select])

        correctbacklash = widgets.Checkbox(value=True, description='Correct Backlash')
        interem_tilts = widgets.FloatText(value=90.0, description='Intermediate Tilt:')
        correct_intermediates = widgets.Checkbox(value=False, description='Correct Intermediate Tilt')  
        interem_pause = widgets.FloatText(value=0.0, description='Intermediate Pause:')
        self.options_group = widgets.VBox([correctbacklash, interem_tilts, correct_intermediates, interem_pause])

        tiltscheme_select.on_click(self._on_tiltscheme)
        
    def show(self):
        self.microscope.image.show()
        self._show_window_settings()
        self._show_experiment_settings()
        confirm_button = widgets.Button(description='Confirm Experiment')
        confirm_button.on_click(self._on_confirm_experiment)

        self.experiment_group = widgets.VBox([self.control_group, self.experiment_type_group, self.options_group, confirm_button])
  
    def _on_confirm_experiment(self, b):
        tiltscheme = TOMOBASE_TILTSCHEMES[self.tiltscheme_group.children[0].value].parsewidget(self.tiltwidget)
        _dict = {
            'tiltscheme': tiltscheme,
            'magnifications': self.experiment_type_group.children[2].value,
            'experiment': self.experiment_type_group.children[0].value,
            'correctbacklash': self.options_group.children[0].value,
            'intermediate_tilt': self.options_group.children[1].value,
            'correct_intermediates': self.options_group.children[2].value,
            'intermediate_pause': self.options_group.children[3].value
        }
        self.microscope.start_experiment(**_dict) 
        self.experiment_group.close()
        
    def start_experiment(self, **kwargs):
        pass

    def _on_tiltscheme(self, b):
        if self.istiltselected:
            self.tiltwidget.close()
        self.istiltselected = True
        self.tiltwidget = TOMOBASE_TILTSCHEMES[self.tiltscheme_group.children[0].value].controller.TiltSchemeWidget()
        display(self.tiltwidget)

    def _on_magnification(self, b):
        if self.state == MicroscopeState.Ready:
            self.threadedrequest(self.set_magnification, self.control_group.children[0].value)

    def set_magnification(self, magnification):
            self.microscope.magnification = magnification

    def _on_blank(self, b):
        print(self.state)
        if self.state == MicroscopeState.Ready:
            self.threadedrequest(self.set_blank, self.control_group.children[1].value)
    
    def set_blank(self, isblanked):
        self.microscope.isblank = isblanked











    


