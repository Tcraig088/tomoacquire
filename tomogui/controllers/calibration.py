import threading
import time
import numpy as np
import pandas as pd

from scipy.optimize import minimize 
  
from .microscope import MicroscopeController


class CalibrationController(MicroscopeController):
    def __init__(self):
        super().__init__()
        self.calibrated = False
        
        self.positions = pd.DataFrame(columns=['a','x','y','c'])
        # These are the calibrations that are used for non changing parameters on the same grid
        self.axial_calibrations = {}
        self.axial_calibrations['theta'] = 0
        self.axial_calibrations['y'] = 0
        self.axial_calibrations['x'] = 0

        
        # Positional Calibrations are calibrations that are changed with the tilt angle.
        self.positional_calibration = {}
        self.positional_calibration['r'] = 0
        self.positional_calibration['alpha_offset'] = 0 
        self.positional_calibration['theta'] = 0
        
    
    def start_calibration(self):
        self.sm.acsleep = self.model.imaging.acquisition_dwell_time*(10**-6)*self.model.imaging.acquisition_frame_size*self.model.imaging.acquisition_frame_size
        self.sm.scansleep  = self.model.imaging.scanning_dwell_time*(10**-6)*self.model.imaging.scanning_frame_size*self.model.imaging.scanning_frame_size
        
        self.sm.start_time =  time.perf_counter()
        self.sm.blanked_time = 0
        
        self.sm.use_running =  False
        self.sm.flag_scanning = True
        self.sm.state_scanning = True
        self.sm.flag_tilting = False
        self.func = self.update_position
        
        self.thread_acquisition = threading.Thread(target=self.acquisition)
        self.thread_tilting =  threading.Thread(target=self.tilting)
        
        self.sm.angles = 0
        
        self.thread_acquisition.start()   
        self.thread_tilting.start()
        

        self.set_scanning_mode()
        
    def update_position(self, image):
        position = self.microscope.Stage.Position
        defocus = self.microscope.Projection.Defocus
        if self.sm.current_angle == 0:
            if self.calibrated:
                pos = self.estimate_initial_position(self.tiltscheme.get_angle(self.sm.angles+1))
            self.positions = pd.DataFrame(columns=['a','x','y','c'])
            self.positions = self.positions.append({'a':position['a'],'x':position['x'],'y':position['y'],'c':defocus}, ignore_index=True)
        elif self.sm.angles>=4:
            self.positions = self.positions.append({'a':position['a'],'x':position['x'],'y':position['y'],'c':defocus}, ignore_index=True)
            self.logger.info('T1: Positions:a %s deg, x %s um, y %s um, f %s nm', np.round(self.tiltscheme.get_angle(self.sm.angles),2), position['x']*(10**6), position['y']*(10**6), defocus*(10**9))
            pos = self.predict_next_position(self.tiltscheme.get_angle(self.sm.angles+1), True)
            self.calibrated = True
            self.logger.info('T1: Estimate: a %s deg, x %s um, y %s um, f %s nm',np.round(self.tiltscheme.get_angle(self.sm.angles+1),2), pos[0]*(10**6), pos[1]*(10**6), pos[2]*(10**9))
        else:
            self.positions = self.positions.append({'a':position['a'],'x':position['x'],'y':position['y'],'c':defocus}, ignore_index=True)
            
            self.logger.info('T1: Positions:a %s deg, x %s um, y %s um, f %s nm', np.round(self.tiltscheme.get_angle(self.sm.angles),2), position['x']*(10**6), position['y']*(10**6), defocus*(10**9))
            pos = self.predict_next_position(self.tiltscheme.get_angle(self.sm.angles+1), True)
            self.logger.info('T1: Estimate: a %s deg, x %s um, y %s um, f %s nm',np.round(self.tiltscheme.get_angle(self.sm.angles+1),2), pos[0]*(10**6), pos[1]*(10**6), pos[2]*(10**9))
        print(self.positions)
    def reset_calibration(self):
        self.calibrated = False
        self.axial_calibrations = {
            'theta': 0, 
            'y': 0,
            'x': 0,
        }
        self.positional_calibration = {
            'r': 0,
            'alpha_offset': 0,
            'theta':0
        }
        self.positions = pd.DataFrame(columns=['a','x','y','c'])
        self.angle = 0

    def predict_next_position(self, angle, update):
        ang = np.radians(angle)
        if update==True:
            estimates = [self.positional_calibration['r'], self.positional_calibration['alpha_offset'], self.positional_calibration['theta'] ]
            print('estimates', estimates[0],estimates[1],estimates[2])
            results = minimize(self.compute_positional_parameters,estimates)
            self.positional_calibration['r'] = results.x[0]
            self.positional_calibration['alpha_offset'] = results.x[1]
            self.positional_calibration['theta'] = results.x[1]
            print('updated', results.x[0],results.x[1],results.x[2])
            
        dx = self.positional_calibration['r']*np.cos(ang+self.positional_calibration['alpha_offset'])*np.sin(self.positional_calibration['theta'])
        dy = self.positional_calibration['r']*np.cos(ang+self.positional_calibration['alpha_offset'])*np.cos(self.positional_calibration['theta'])
        dz = self.positional_calibration['r']*np.sin(ang+self.positional_calibration['alpha_offset'])
        
        # get zero position
        x0 = self.positional_calibration['r']*np.cos(0)*np.sin(self.positional_calibration['theta'])
        y0 = self.positional_calibration['r']*np.cos(0)*np.cos(self.positional_calibration['theta'])
        z0 = self.positional_calibration['r']*np.sin(0)
        
        x = x0 + dx
        y = y0 + dy
        defocus = z0 + dz
        return [x, y, defocus]
    
    # TODO: it'd be nice to estimate the quality of this fit
    def estimate_initial_position(self, pos):
        pos = self.predict_next_position(0, False)
        self.axial_calibrations['x'] = pos[0] - (self.positional_calibration['r']*np.sin(self.positional_calibration['theta']))
        self.axial_calibrations['y'] = pos[1] - (self.positional_calibration['r']*np.cos(self.positional_calibration['theta']))
        self.axial_calibrations['theta'] = self.positional_calibration['theta']
        
        m1, m2 = 1/np.tan(self.axial_calibrations['theta']), np.tan(self.axial_calibrations['theta']) 
        c1, c2 = self.axial_calibrations['y']-(m1*self.axial_calibrations['x']), self.axial_calibrations['y']-(m2*self.axial_calibrations['x'])
        x = (c1 - c2)/(m2 -m1)
        y = x/np.tan(self.axial_calibrations['theta'])
        r_component = np.sqrt(((pos['x']-x)**2)+((pos['y']-y)**2))
        z = 0
        self.positional_calibration['alpha_offset'] = np.arctan(z/r_component)
        self.positional_calibration['r'] = np.sqrt((z**2)+(r_component**2))
        
    def compute_positional_parameters(self, params):
        displacements = self.positions
        first_row = displacements.iloc[0]
        displacements = displacements.diff().fillna(first_row)
        
        r, alpha_offset, theta = params
        dx = ((r*np.cos(displacements['a']+alpha_offset))*np.sin(theta))-((r*np.cos(alpha_offset))*np.sin(theta))
        dy = ((r*np.cos(displacements['a']+alpha_offset))*np.cos(theta))-((r*np.cos(alpha_offset))*np.cos(theta))
        #print(dx, dy, displacements['x'], displacements['y'])
        return np.sum(((dx-displacements['x'])**2) +((dy-displacements['y'])**2))







        
    
    