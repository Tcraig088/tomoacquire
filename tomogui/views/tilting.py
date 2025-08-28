import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class MagTrackScheme(tk.Frame):
    def __init__(self, parent):
        self.TrackMagLabel =tk.label(self, text = 'Tracking Magnification (kx')
        self.TrackMagValue = tk.Spinbox(self, from_=5, to=30000,increment=1)
        self.ImagingMagLabel =tk.label(self, text = 'Imaging Magnification (kx')
        self.ImagingMagValue = tk.Spinbox(self, from_=5, to=30000,increment=1)     
        
        self.TrackMagLabel.grid(row=0, column=0, sticky='w')
        self.TrackMagValue.grid(row=0, column=1, sticky='w')
        self.ImagingMagLabel.grid(row=0, column=2, sticky='w')
        self.ImagingMagValue.grid(row=0, column=3, sticky='w')

class TrackingScheme(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        options =  ['Manual','Magnification Switching']
        self.TypeLabel =  tk.Label(self, text='Tracking Method')
        self.ComboBox =ttk.Combobox(self, values = options)
        
class BDScheme(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.StartLabel = tk.Label(self, text='Start Angle (deg):')
        self.EndLabel = tk.Label(self, text='End Angle (deg):')
        self.KLabel = tk.Label(self, text='k:')
        self.StartSpinBox = tk.Spinbox(self, from_=-90, to=90, increment=0.1)
        self.EndSpinBox = tk.Spinbox(self, from_=-90, to=90, increment=0.1)
        self.KSpinBox = tk.Spinbox(self, from_=0, to=100, increment=0.1)
        
        
        self.StartSpinBox.delete(0, 'end')
        self.StartSpinBox.insert(0, '-70')
        self.EndSpinBox.delete(0, 'end')
        self.EndSpinBox.insert(0, '70')
        self.KSpinBox.delete(0, 'end')
        self.KSpinBox.insert(0, '8')
        
        self.StartLabel.grid(row=0, column=0, sticky='w')
        self.StartSpinBox.grid(row=0, column=1, sticky='w')
        self.EndLabel.grid(row=0, column=2, sticky='w')
        self.EndSpinBox.grid(row=0, column=3, sticky='w') 
        self.KLabel.grid(row=0, column=4, sticky='w')
        self.KSpinBox.grid(row=0, column=5, sticky='w') 
        
        
class GRSScheme(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.StartLabel = tk.Label(self, text='Start Angle (deg):')
        self.EndLabel = tk.Label(self, text='End Angle (deg):')
        self.StartSpinBox = tk.Spinbox(self, from_=-90, to=90, increment=0.1)
        self.EndSpinBox = tk.Spinbox(self, from_=-90, to=90, increment=0.1)
        self.StartSpinBox.delete(0, 'end')
        self.StartSpinBox.insert(0, '-70')
        self.EndSpinBox.delete(0, 'end')
        self.EndSpinBox.insert(0, '70')
        
        self.StartLabel.grid(row=0, column=0, sticky='w')
        self.StartSpinBox.grid(row=0, column=1, sticky='w')
        self.EndLabel.grid(row=0, column=2, sticky='w')
        self.EndSpinBox.grid(row=0, column=3, sticky='w')

        
class IncrementalScheme(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.StartLabel = tk.Label(self, text='Start Angle (deg):')
        self.EndLabel = tk.Label(self, text='End Angle (deg):')
        self.IncrementLabel = tk.Label(self, text='Step (deg):')
        self.StartSpinBox = tk.Spinbox(self, from_=-90, to=90, increment=0.5)
        self.EndSpinBox = tk.Spinbox(self, from_=-90, to=90, increment=0.5)
        self.StepSpinBox = tk.Spinbox(self, from_=0.5, to=90, increment=0.5)
        self.StartSpinBox.delete(0, 'end')
        self.StartSpinBox.insert(0, '-70')
        self.EndSpinBox.delete(0, 'end')
        self.EndSpinBox.insert(0, '70')
        self.StepSpinBox.delete(0, 'end')
        self.StepSpinBox.insert(0, '2.0')
        
        self.StartLabel.grid(row=0, column=0, sticky='w')
        self.StartSpinBox.grid(row=0, column=1, sticky='w')
        self.EndLabel.grid(row=0, column=2, sticky='w')
        self.EndSpinBox.grid(row=0, column=3, sticky='w')
        self.IncrementLabel.grid(row=1, column=0, sticky='w')
        self.StepSpinBox.grid(row=1, column=1, sticky='w')

class TiltScheme(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Tilt Scheme', padx=10, pady=10)
        self.label = tk.Label(self, text='Tilt Scheme : Golden Ratio')
        
        self.GRSWidget = GRSScheme(self)    
        self.IncrementalWidget = IncrementalScheme(self)
        self.BDWidget = BDScheme(self)
        
        self.label.grid(row=0, column=0, sticky='w')
        self.GRSWidget.grid(row=1, column=0, sticky='w')
        self.IncrementalWidget.grid(row=1, column=0, sticky='w')
        self.BDWidget.grid(row=1, column=0, sticky='w')
        
        self.BDWidget.grid_remove()
        self.IncrementalWidget.grid_remove()
        self.pack(fill=tk.X)

class FileEntry(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        padx=2
        self.filename = tk.StringVar()
        self.FileLabel = tk.Label(self, text='File :')
        self.FileEntry = tk.Entry(self, textvariable = self.filename)
        self.FileButton = tk.Button(self, text='Browse', command=self.savefiledialog)
        
        self.FileLabel.pack(padx=padx,side=tk.LEFT)
        self.FileEntry.pack(padx=padx,side=tk.LEFT)
        self.FileButton.pack(padx =padx, side=tk.LEFT)
     
    def savefiledialog(self):
        self.filename.set(filedialog.asksaveasfilename(defaultextension='.h5', filetypes=[('HDF5 files', '*.h5')], title='Save File As...'))

        
class Settings(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='CollectionSettings', padx=10, pady=10)
        self.FileEntryWidget = FileEntry(self)
        
        self.selected_option = tk.StringVar()
        self.selected_option.set('GRS')
        self.grsRadioButton = tk.Radiobutton(self, text='Golden Ratio', variable=self.selected_option, value='GRS')
        self.incrementalRadioButton = tk.Radiobutton(self, text='Incremental', variable=self.selected_option, value='Incremental')
        self.BDRadioButton = tk.Radiobutton(self, text='Binary', variable=self.selected_option, value='Binary')
        
        self.FileEntryWidget.pack(anchor=tk.W)
        self.grsRadioButton.pack(anchor=tk.W)
        self.incrementalRadioButton.pack(anchor=tk.W)
        self.BDRadioButton.pack(anchor=tk.W)
        
        self.pack(fill=tk.X)

class Fasttomography(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.Pauselabel = tk.Label(self, text='Pause (s)')
        self.PauseSpinBox = tk.Spinbox(self, from_=1, to=1000, increment=0.5)  
        
        self.hightiltlabel = tk.Label(self, text='High Tilt Angle (deg)')    
        self.HighTiltSpinBox = tk.Spinbox(self, from_=0, to=90, increment=0.5)
        self.HighTiltSpinBox.delete(0, 'end')
        self.HighTiltSpinBox.insert(0, '50')
        
        self.hightiltpauselabel = tk.Label(self, text='High Tilt Pause (s)')
        self.HighTiltPauseSpinBox = tk.Spinbox(self, from_=1, to=1000, increment=0.5)
        
        self.Pauselabel.grid(row=0, column=0, sticky='w')
        self.PauseSpinBox.grid(row=0, column=1, sticky='w')
        self.hightiltlabel.grid(row=1, column=0, sticky='w')
        self.HighTiltSpinBox.grid(row=1, column=1, sticky='w')
        self.hightiltpauselabel.grid(row=2, column=0, sticky='w')
        self.HighTiltPauseSpinBox.grid(row=2, column=1, sticky='w')
        
        
class AdvancedSettings(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='CollectionSettings', padx=10, pady=10)
        
        self.fasttomo_var = tk.IntVar(value=0)
        self.FastomoCheckBox = tk.Checkbutton(self, text='Fast Tomo Mode', variable=self.fasttomo_var, command=self.toggle_fasttomo)
        
        self.usemanual_var = tk.IntVar(value=0) 
        self.ManualTiltCheckBox = tk.Checkbutton(self, text='Manual Track and Focus', variable=self.usemanual_var)
        
        self.backlashcorrect_var = tk.IntVar(value=1)
        self.BacklashCheckBox = tk.Checkbutton(self, text='Backlash Compensation', variable=self.backlashcorrect_var)
        
        self.comcorrect_var = tk.IntVar(value=0)
        self.comcorrectionCheckBox = tk.Checkbutton(self, text='Centre of Mass Correction', variable=self.comcorrect_var)
        
        self.FasttomoWidget = Fasttomography(self)
        
        self.FastomoCheckBox.grid(row=0, column=0, sticky='w')
        self.ManualTiltCheckBox.grid(row=0, column=1, sticky='w')
        self.BacklashCheckBox.grid(row=1, column=0, sticky='w')
        self.comcorrectionCheckBox.grid(row=1, column=1, sticky='w')
        self.FasttomoWidget.grid(row=2, column=0,columnspan=6, sticky='w')

        self.FasttomoWidget.grid_remove()
        
        self.pack(fill=tk.X)
        
    def toggle_fasttomo(self):
        if self.fasttomo_var.get():
            self.FasttomoWidget.grid()
        else:
            self.FasttomoWidget.grid_remove()

class Submitter(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Confirm Values', padx=10, pady=10)
        self.SubmitButton = tk.Button(self, text='Confirm')
        self.SubmitButton.pack(anchor=tk.W)
        self.pack(fill=tk.X)
        
class BaseFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Settings = Settings(self)
        self.TiltScheme = TiltScheme(self)
        self.AdvancedSettings = AdvancedSettings(self)
        self.Submitter = Submitter(self)
        
        self.Settings.pack(fill=tk.X)
        self.TiltScheme.pack(fill=tk.X)
        self.AdvancedSettings.pack(fill=tk.X)
        self.Submitter.pack(fill=tk.X)
        
        self.Settings.selected_option.trace('w', self.switch_scheme)
        #self.combo_var.trace('w', self.switch_widget)
        self.pack(fill=tk.X)
        
    def switch_scheme(self, *args):
        if self.Settings.selected_option.get() == 'GRS':
            #Set label to 'Tilt Scheme Golden Ratio'
            self.TiltScheme.label.config(text='Tilt Scheme : Golden Ratio')
            self.TiltScheme.GRSWidget.grid()
            self.TiltScheme.BDWidget.grid_remove()
            self.TiltScheme.IncrementalWidget.grid_remove()
        elif self.Settings.selected_option.get() == 'Incremental':
            self.TiltScheme.label.config(text='Tilt Scheme : Incremental Acquisition')
            self.TiltScheme.GRSWidget.grid_remove()
            self.TiltScheme.BDWidget.grid_remove()
            self.TiltScheme.IncrementalWidget.grid()
        elif self.Settings.selected_option.get() == 'Binary':
            self.TiltScheme.label.config(text='Tilt Scheme : Binary')
            self.TiltScheme.GRSWidget.grid_remove()
            self.TiltScheme.IncrementalWidget.grid_remove()
            self.TiltScheme.BDWidget.grid()