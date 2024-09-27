from qtpy.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout, QLineEdit, QVBoxLayout, QPushButton, QGridLayout, QDoubleSpinBox
from qtpy.QtCore import Qt

from tomobase.napari.components import CheckableComboBox, CollapsableWidget

class ScanSettingsWidget(CollapsableWidget):
    def __init__(self, title, parent):
        super().__init__(parent, title)
        self.label_dwell_time = QLabel('Dwell Time (\u03BCs):')
        self.double_spinbox_dwell_time = QDoubleSpinBox()
        self.double_spinbox_dwell_time.setSingleStep(0.01)
        self.double_spinbox_dwell_time.setValue(1.0)
        self.label_frame_size = QLabel('Frame Size (px):')
        self.combobox_frame_size = QComboBox()
        self.label_frame_time= QLabel('Frame Time (s):')
        self.double_spinbox_frame_time = QDoubleSpinBox()
        self.double_spinbox_frame_time.setSingleStep(0.01)
        self.double_spinbox_frame_time.setValue(1.0)
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.label_dwell_time, 0, 0)
        self.layout.addWidget(self.double_spinbox_dwell_time, 0, 1)
        self.layout.addWidget(self.label_frame_size, 1, 0)
        self.layout.addWidget(self.combobox_frame_size, 1, 1)
        self.layout.addWidget(self.label_frame_time, 2, 0)
        self.layout.addWidget(self.double_spinbox_frame_time, 2, 1)
        
        self.setLayout(self.layout)
        
        
class CustomConnectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.label_name = QLabel('Name:')
        self.lineedit_name = QLineEdit('Microscope')
        self.label_connection = QLabel('Address:')
        self.lineedit_connection = QLineEdit('localhost')
        self.label_socket_request = QLabel('Request Socket:')
        self.lineedit_request = QLineEdit('50030')
        self.label_socket_reply = QLabel('Reply Socket:')
        self.lineedit_socket_reply = QLineEdit('50031')
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.label_name, 0, 0)
        self.layout.addWidget(self.lineedit_name, 0, 1)
        self.layout.addWidget(self.label_connection, 0, 2 )
        self.layout.addWidget(self.lineedit_connection, 0, 3)
        self.layout.addWidget(self.label_socket_request, 1, 0)
        self.layout.addWidget(self.lineedit_request, 1, 1)
        self.layout.addWidget(self.label_socket_reply, 1, 2)
        self.layout.addWidget(self.lineedit_socket_reply, 1, 3)
        
        self.layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.layout)
        
class InstrumentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.combobox = QComboBox()
        #TODO: check for registed microscope configs
        self.combobox.addItem('Select Microscope')
        self.combobox.addItem('Custom')
        self.connection_widget = CustomConnectionWidget()
        self.button_connect = QPushButton('Connect')
        self.button_save = QPushButton('Save')
        self.connection_widget.setVisible(False)
        self.button_save.setVisible(False)
        
        self.combobox_options = CheckableComboBox(self)
        self.combobox_options.addItem("Select Options")
        self.combobox_options.addItem("Manual Frame Time")
        self.combobox_options.addItem("Correct Backlash")
        self.combobox_options.addItem("Manual Screen Current")
        
        self.combobox_detectors = CheckableComboBox(self)
        self.combobox_detectors.addItem("Select Detectors")

        self.acquisition_settings = ScanSettingsWidget('Acquisition Settings:', self)  
        self.scan_settings = ScanSettingsWidget('Scanning Settings:', self)
        
        self.button_confirm = QPushButton('Confirm')   
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.combobox, 1, 0)
        self.layout.addWidget(self.connection_widget, 1, 0, 1, 2)
        self.layout.addWidget(self.button_connect, 2, 0)
        self.layout.addWidget(self.button_save, 2, 1)
        
        self.layout.addWidget(self.combobox_options, 3, 0)
        self.layout.addWidget(self.combobox_detectors, 4, 0)
        
        self.layout.addWidget(self.acquisition_settings, 5, 0, 1, 2)
        self.layout.addWidget(self.scan_settings, 6, 0, 1, 2)
        
        self.layout.addWidget(self.button_confirm, 7, 0, 1, 2)

        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.on_combobox_change)
        self.button_connect.clicked.connect(self.on_connect)
        
        
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
    
    