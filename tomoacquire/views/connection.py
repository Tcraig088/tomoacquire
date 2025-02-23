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

class ConnectView():
    def __init__(self, controller):
        self.controller = controller
        self.show()
        
    def show(self):
        microscopes_dropdown = widgets.Dropdown(options = mc.get_names())
        connect_button = widgets.Button(description='Connect')
        self.connect_group = widgets.HBox([microscopes_dropdown, connect_button])
        connect_button.on_click(self._on_connect)
        display(self.connect_group)

    def _on_connect(self, b):
        microscope_name = self.connect_group.children[0].value
        self.controller.connect(microscope_name)
        self.connect_group.close()


