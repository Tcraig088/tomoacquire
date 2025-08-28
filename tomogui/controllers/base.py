from tomogui.controllers import experiment, calibration
import tkinter as tk


class Controller(experiment.ExperimentController):
    def __init__(self):
        super().__init__()

        self.view.ImagingFrame.Submitter.SubmitButton.config(command=self.set_imaging_model)
        self.view.TomographyFrame.Submitter.SubmitButton.config(command=self.set_tilt_model)
        
        self.view.ExperimentFrame.Submitter.SubmitButton.config(command=self.start_stop_experiment)
        self.view.ExperimentFrame.Submitter.NextAngleButton.config(command=self.tilt_to_next_angle)
        
        self.view.CalibrationFrame.Submitter.SubmitButton.config(command=self.start_stop_calibration)
        self.view.CalibrationFrame.Submitter.NextAngleButton.config(command=self.tilt_to_next_angle)
        self.view.CalibrationFrame.Submitter.NextParticleButton.config(command=self.next_particle)
        self.view.CalibrationFrame.Submitter.ResetButton.config(command=self.reset_calibration)

        
        self.view.protocol("WM_DELETE_WINDOW", self.on_close)
        #self.view.ExperimentFrame.Submitter.NextAngleButton.config(command=self.model.next_angle)
    
    """_set the tilting paramaters on confirmation_
    """
    def set_tilt_model(self):
        if self.state_check(0,0):
            self.model.tilting.set(self.view.TomographyFrame)
            self.sm.state_config_tilting = True
            self.logger.info('Setting Tilting Data')    
    """_set the imaging paramaters on confirmation_
    """            
    def set_imaging_model(self):
        if self.state_check(0,0):
            self.model.imaging.set(self.view.ImagingFrame)
            self.set_instrument()
            self.sm.state_config_imaging = True
            self.logger.info('Setting Imaging Data')  
            print(self.model.imaging.scanning_dwell_time)
    """Close the application and stop the threads
    """  
    def on_close(self):
        if self.state_check(0):
            self.view.destroy()
    
    def start_stop_calibration(self):
        if self.sm.state_calibrating:
            self.sm.state_calibrating = False
            self.view.CalibrationFrame.Submitter.NextAngleButton.pack_forget()
            self.view.CalibrationFrame.Submitter.NextParticleButton.pack_forget()
            self.view.CalibrationFrame.Submitter.ResetButton.pack(padx=2, side=tk.LEFT)
            self.view.CalibrationFrame.Submitter.SubmitButton.config(text='Start')
        else:
            if not self.state_check(1,1):
                return
            self.view.CalibrationFrame.Submitter.SubmitButton.config(text='Stop')
            self.view.CalibrationFrame.Submitter.NextAngleButton.pack(padx=2, side=tk.LEFT)
            self.view.CalibrationFrame.Submitter.NextParticleButton.pack(padx=2, side=tk.LEFT)
            self.view.CalibrationFrame.Submitter.ResetButton.pack_forget()
            
            #Initialise Thread  
            self.sm.state_calibrating = True
            self.start_calibration()


    
    def start_stop_experiment(self):
        #Change Start to stop button
        if self.sm.state_running:
            self.sm.state_running = False
            self.view.ExperimentFrame.Submitter.NextAngleButton.pack_forget()
            self.view.ExperimentFrame.Submitter.SubmitButton.config(text='Start')
        else:
            if not self.state_check(1,2):
                return
            
            self.view.ExperimentFrame.Submitter.SubmitButton.config(text='Stop')
            if self.model.tilting.fasttomo:
                self.view.ExperimentFrame.Submitter.NextAngleButton.pack_forget()
            else:
                self.view.ExperimentFrame.Submitter.NextAngleButton.pack(padx = 2, side=tk.LEFT) 
            self.sm.state_running = True
            self.start_experiment()
            
    def tilt_to_next_angle(self):
        self.sm.flag_scanning = False

    def next_particle(self):
        self.flag_particle = True

         

            
        
    
