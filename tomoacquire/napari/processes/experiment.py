from qtpy.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout, QLineEdit, QVBoxLayout, QPushButton, QGridLayout, QDoubleSpinBox
from qtpy.QtCore import Qt

from tomobase.napari.components import CheckableComboBox, FileSaveDialog
        
class ExperimentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filedialog = FileSaveDialog()
        self.filedialog.set_extensions(mrc='Medical Research Council', tiff='Tagged Image File Format')
        
        self.label_maginification = QLabel('Magnification:')
        self.combobox_maginification = QComboBox()
        self.combobox_maginification.addItem('Select Magnification')
        self.combobox_options = CheckableComboBox(self)
        self.combobox_options.addItem("Select Options")
        
        self.label_tiltscheme = QLabel('Tilt Scheme:')  
        self.combobox_tiltscheme = QComboBox()
        self.combobox_tiltscheme.addItem('Select Tilt Scheme')
        self.combobox_tiltscheme.setCurrentIndex(0)
        
        self.button_confirm = QPushButton('Confirm')
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.filedialog, 0, 0, 1, 3)
        self.layout.addWidget(self.label_maginification, 1, 0)
        self.layout.addWidget(self.combobox_maginification, 1, 1)
        self.layout.addWidget(self.combobox_options, 2, 0)
        self.layout.addWidget(self.label_tiltscheme, 2, 0)
        self.layout.addWidget(self.combobox_tiltscheme, 3, 1)
        
        self.layout.addWidget(self.button_confirm, 5, 0)

        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        
    def on_combobox_change(self, index):
        if self.combobox.currentText() == 'Custom':
            self.connection_widget.setVisible(True)
            self.button_save.setVisible(True)
        else:
            self.connection_widget.setVisible(False)
            self.button_save.setVisible(False)
    
    def on_connect(self):
        #TODO: connect to microscope
        pass
    
    def on_save(self):
        #TODO: save connection
        pass
    
    