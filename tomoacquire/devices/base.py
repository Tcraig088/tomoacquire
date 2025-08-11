import zmq
from tomoacquire import config

class DeviceController:
    def __init__(self, name= 'New Microscope', address='localhost', request=50000):
        self.name = name
        
        self.context = zmq.context()
        self.request_address = f"tcp://{address}:{request}"
        self.request_socket = self.context.socket(zmq.REQ)
        
        
    def connect(self):
        self.request_socket.connect(self.request_address)
        
        
    def disconnect(self):
        self.request_socket.close()
        self.context.term()
        
    @classmethod
    def register(cls, name, address='localhost', request=50000, **kwaargs):
        _dict = {
            'type': cls.tomobase_name,
            'name': name,
            'address': address,
            'request': request
        }
        for key, value in kwaargs.items():
            _dict[key] = value

        config.add_microscope(_dict)
