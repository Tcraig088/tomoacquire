import numpy as np
import time
import os 
import temscript 
import h5py

from tomogui.dummy import Dummy
from tkinter import messagebox

from ..models import base as mbase
from ..views import base as vbase
from .. import logs

class DoseSymmetric():
    def __init__(self):
        self.start = -70
        self.end = 70
        self.step = 5
        
    def get_angle(self, i):
        # if i is even
        val = (i+1)//2
        if (i+1)%2 == 1:
            ang = val*self.step
        else:
            ang = -1*val*self.step
        return ang
    
    def isfinished(self, angle):
        if angle <= self.start:
            return True
        else:
            return False
        
class StateMachine:
    def __init__(self):
        self.use_running = False
        self.state_running =  False
        self.state_scanning = False
        self.state_calibrating = False
        
        self.state_config_imaging = False
        self.state_config_tilting = False
        
        self.active_threads = 0
        
        self.flag_scanning = False
        self.flag_tilting = False
        
        self.start_time = 0
        self.blanked_time = 0   
        self.angles = 0
        self.images = 0 
        self.acsleep = 1
        self.scansleep = 1
        self.current_angle =0 
        self.debug = False
        
class MicroscopeController(logs.Log):
    def __init__(self): 
        super().__init__() 
        self.sm = StateMachine()
        self.view = vbase.View()
        self.model = mbase.Model()

    def get_time(self):
        t = time.perf_counter() - self.sm.start_time
        exp_time  = t -  self.sm.blanked_time
        return [t, exp_time]
    
    def set_instrument(self):
        if self.model.imaging.dummy:
            self.microscope = Dummy()
            self.debug = True
        else:
            self.microscope = temscript.GetInstrument()
            self.debug = False
            self.microscope.Acquisition.AddAcqDeviceByName('HAADF')

    def set_scanning_mode(self):
        if self.sm.state_scanning:
            self.microscope.Acquisition.StemAcqParams.DwellTime = self.model.imaging.scanning_dwell_time*(10**-6)
            self.microscope.Acquisition.StemAcqParams.Binning = 2048/self.model.imaging.scanning_frame_size
        else:
            self.microscope.Acquisition.StemAcqParams.DwellTime = self.model.imaging.acquisition_dwell_time*(10**-6)
            self.microscope.Acquisition.StemAcqParams.Binning = 2048/self.model.imaging.acquisition_frame_size
                 
    def switch_scanning_mode(self, acq=False):
        if self.sm.state_scanning != acq:
            self.sm.state_scanning = acq
            self.set_scanning_mode()
        else:
            return
    
    def acquire(self):
        angle = np.round(np.degrees(self.microscope.Stage.Position['a']),2)
        images = self.microscope.Acquisition.AcquireImages()
        if self.sm.state_scanning:
            time.sleep(self.sm.scansleep)
        else:
            time.sleep(self.sm.acsleep)
        t = self.get_time()
        image_dict = {}
        
        if isinstance(images,list):
            for item in images:
                image_dict[item.Name] = item.Array
        else:
            image_dict[images.Name] = images.Array
        image_dict['acquisition timee (s)'] = t[0]
        image_dict['exposure time (s)'] = t[1]
        image_dict['alpha tilt (deg)'] = angle
        
        return image_dict
    
    
    """_summary_
    
    Thread safety is really important. This will check the states of the microscope and perform any necessary actions.

    """
    def state_check(self, securitylevel=0, config_required = 0 ):
        flag = True
        #Security level 0 is for processes that cannot be performed while the microscope is running
        if securitylevel == 0 :
            
            if self.sm.state_running:
                flag=False
                msg = 'Cannot perform this action during an active experiment. Please stop the experiment first.'
            if self.sm.state_calibrating:
                flag=False
                msg = 'Cannot perform this action during an active callibration. Please stop the callibration first.'
            elif self.sm.active_threads > 0:
                flag = False
                msg = """Please Wait. Cannot perform this action because the microscope is currently active. 
                        Calllibration or Experiments take some time to exit after stopping."""


        # Security level 1 is just you cannot run while there are active threads
        if securitylevel == 1:
            if self.sm.active_threads > 0:
                flag = False
                msg = """Cannot Start a process while there is an active process running. 
                        Check to make sure both the callibration and the experiment processes are stopped.
                        If they are both off just wait a few seconds and try again. Process take some time to exit after stopping."""
        
        
        if config_required >= 1:
            if not self.sm.state_config_imaging:
                flag = False
                msg = 'Cannot perform this action without configuring the imaging parameters first.'
        if config_required >= 2:
            if not self.sm.state_config_tilting:
                flag = False
                msg = 'Cannot perform this action without configuring the tilting parameters first.'
                
                
        if flag == False:
            messagebox.showinfo('Error', msg)
                
        return flag
    
    def change_position(self, angle):
        ang = np.radians(np.round(angle,2))
        position = self.microscope.Stage.Position
        if self.model.tilting.backlashcorrect:
            correction = np.radians(2)
            if position['a'] > ang:
                self.wrapped_go_to(ang-correction)
                time.sleep(0.01)
                self.wrapped_go_to(ang)
            elif position['a'] < ang:
                self.wrapped_go_to(ang)
            else:   
                self.logger.warning('No change required')
                
            self.sm.angles += 1
            self.logger.info('Angle set to: %s', str(np.round(angle, 2)))
            self.view.ExperimentFrame.Summary.angles_val.set(np.round(angle,2))
            
    def wrapped_go_to(self,ang):
        worked = False
        while(worked==False):
            try:
                self.microscope.Stage.GoTo(a=ang)
                worked = True
            except:
                time.sleep(0.2)
                    
    def end_sm_state(self):
        if self.sm.use_running:
            self.sm.state_running = False
            return self.sm.state_running
        else:
            self.sm.state_callibrating = False
            return self.sm.state_calibrating
        
    def check_sm_state(self):
        if self.sm.use_running:
            return self.sm.state_running
        else:
            return self.sm.state_calibrating
        
    def tilting(self):
        self.sm.angles = 0 
        self.sm.active_threads +=1
        self.logger.info('Started Tilting Thread')
        if self.sm.use_running:
            self.tiltscheme = self.model.tilting.tiltscheme
            if self.model.tilting.fasttomo:
                fasttomo = True
            else:
                fasttomo = False
        else:
            fasttomo =  False
            self.tiltscheme =  DoseSymmetric()
        active_state = self.check_sm_state()
        while active_state:
            if fasttomo:
                self.sm.current_angle = self.tiltscheme.get_angle(self.sm.angles)
                pause = self.model.tilting.pause
                if np.abs(self.sm.current_angle)>=np.abs(self.model.tilting.hightiltangle):
                    pause = self.model.tilting.hightiltpause
                time.sleep(pause)
                self.change_position(self.sm.current_angle)
            else:
                if self.sm.flag_tilting:
                    self.sm.current_angle = self.tiltscheme.get_angle(self.sm.angles)
                    self.change_position(self.sm.current_angle)
                    self.sm.flag_tilting = False
                    self.logger.info('New Angle %s %s', self.sm.current_angle, self.sm.angles)
            if self.tiltscheme.isfinished(self.tiltscheme.get_angle(self.sm.angles)):
                active_state = self.end_sm_state()
            active_state = self.check_sm_state()

        self.change_position(0)
        self.current_angle = 0
        self.sm.active_threads -= 1
        self.logger.info('Ended Tilting Thread')


    def acquisition(self):
        self.sm.active_threads += 1
        self.logger.info('Started Acquisition Thread')
        if self.sm.use_running:
            if self.model.tilting.fasttomo:
                fasttomo = True
            else:
                fasttomo = False
        else:
            fasttomo =  False
        active_state = self.check_sm_state()
        
        while active_state:
            if fasttomo:
                images = self.acquire()
                self.sm.images +=1
                self.func(images)
            else:
                self.switch_scanning_mode(self.sm.flag_scanning)
                if not self.sm.state_scanning:
                    images = self.acquire()
                    self.view.ExperimentFrame.Summary.images_val.set(self.sm.images)
                    self.func(images)
                    self.sm.flag_tilting = True
                    self.sm.images += 1
                    self.logger.info('Acquired %s images', self.sm.images)
                    self.sm.flag_scanning = True
                else:
                    images = self.acquire()
            active_state = self.check_sm_state()

        self.sm.active_threads -= 1
        self.logger.info('Ended Acquisition Thread')

            
            
    

    

    