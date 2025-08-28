import threading
import time
import os
import numpy as np
import h5py

from .calibration import CalibrationController

class ExperimentController(CalibrationController):
    def __init__(self):
        super().__init__()
        self.save_file = ''
        self.image_buffer = []
        pass
    
    def start_experiment(self):
        self.sm.acsleep = self.model.imaging.acquisition_dwell_time*(10**-6)*self.model.imaging.acquisition_frame_size*self.model.imaging.acquisition_frame_size
        self.sm.scansleep  = self.model.imaging.scanning_dwell_time*(10**-6)*self.model.imaging.scanning_frame_size*self.model.imaging.scanning_frame_size
        
        self.sm.acsleep = 2.53
        self.sm.scansleep  = 1.02
 
        
        self.sm.start_time =  time.perf_counter()
        self.sm.blanked_time = 0
        self.sm.images = 0
        self.sm.angles = 0 
        self.sm.use_running = True
        self.sm.state_running = True
        
        self.init_image_buffer()
        self.func = self.add_image_to_buffer
        
        if self.model.tilting.fasttomo:
            self.sm.state_scanning = False
            
        else: 
            self.sm.state_scanning =  True
        self.thread_tilting = threading.Thread(target=self.tilting)
        self.thread_acquisition = threading.Thread(target=self.acquisition)
        self.thread_buffering = threading.Thread(target=self.buffer_images)
            
        self.thread_tilting.start()
        self.thread_acquisition.start()
        self.thread_buffering.start() 

        self.set_scanning_mode()
            

    def add_image_to_buffer(self, image):
        self.image_buffer.append(image)
        
    def init_image_buffer(self):
        if os.path.exists(self.model.tilting.file):
            direc, base = os.path.split(self.model.tilting.file) 
            base, ext = os.path.splitext(base)
            self.save_file = os.path.join(direc, base +'temp-'+str(np.random.randint(1, 1000))+ ext)
        else:
            self.save_file = self.model.tilting.file
        
        self.logger.info('Saving to: '+self.save_file)
        self.new_file = True
        self.image_buffer = []
        self.check_image_buffer()
        
    def buffer_images(self):
        self.sm.active_threads += 1
        self.logger.info('T1: Imaging Buffering Started: %s active threads.', str(self.sm.active_threads))
        while self.sm.state_running:
            self.check_image_buffer()
            time.sleep(2)
        self.sm.active_threads -= 1
        self.logger.info('T1: Imaging Buffering Ended:  %s active threads.', str(self.sm.active_threads))
        
    def check_image_buffer(self):
        nimages = len(self.image_buffer)
        if self.new_file:
            metadata = self.model.to_dict()
            with h5py.File(self.save_file, 'w') as f:
                #self.logger.debug('T1 - Saving Metadata')
                for key1, value1 in metadata.items():
                    #self.logger.debug('T1 - metadata: {key1}' )
                    group = f.create_group('metadata ' + key1)
                    for key, value in metadata[key1].items():
                        #self.logger.debug('T1 - m: {key1}.{key}: {value}' )
                        group.create_dataset(key, data=value)
            self.new_file = False
        if nimages > 0:
            self.logger.info('T1: Saving: '+str(nimages)+' images')
            with h5py.File(self.save_file, 'a') as f:
                for i in range(nimages):
                    self.logger.debug('T1 - Saving Image %s',str((self.sm.images-nimages)+i))
                    group = f.create_group('image '+str((self.sm.images-nimages)+i))
                    for key, value in self.image_buffer[i].items():
                        if isinstance(value, np.ndarray):
                            pass
                            #self.logger.debug('T1 - i: {key}: shape: {value.shape}')
                        else:
                            pass
                            #self.logger.debug(f'T1 - i: {key}: {value}')
                        group.create_dataset(key, data=value)            
            del self.image_buffer[:nimages]