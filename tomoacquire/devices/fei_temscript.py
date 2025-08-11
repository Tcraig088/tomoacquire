
from tomoacquire.devices.base import DeviceController
from tomoacquire.hooks import device_hook

@device_hook(name="FEI Microscope")
class FEIController(DeviceController):
    """Controller for FEI microscopes using TEMScript."""
    
    def __init__(self, name='FEI Microscope', address='localhost', request=50000):
        super().__init__(name=name, address=address, request=request)
        self.name = name
        self.address = address
        self.request_address = f"tcp://{address}:{request}"
        
    def connect(self):
        """Connect to the FEI microscope."""
        super().connect()
        # Additional connection logic specific to FEI microscopes can be added here.
        
    def disconnect(self):
        """Disconnect from the FEI microscope."""
        super().disconnect()
        # Additional disconnection logic specific to FEI microscopes can be added here.