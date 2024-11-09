import json
import os 
import tomop

from tomobase.log import logger

class Microscope():
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Microscope, cls).__new__(cls)
        return cls._instance

    def __init__(self, name:str = 'Microscope', address:str='localhost', request:int='50030', subscribe:int='50031'):
        self.isconnected = False
        
        self.name = 'Microscope'
        self.address = 'localhost'
        self.request = '50030'
        self.subscribe = '50031'
        
    def to_json(self, path:str):
        data = {}
        data['name'] = self.name
        data['address'] = self.address
        data['request'] = self.request
        data['subscribe'] = self.subscribe
        
        filepath = os.path.join(path, self.name.replace(' ','_') + '.json')
        if os.path.exists(filepath):
            logger.warning(f'File {filepath} already exists. Overwriting.')
            os.remove(filepath)
        with open(filepath, 'w') as f:
            json.dump(data, f)

    @classmethod 
    def from_json(cls, path:str):
        with open(path, 'r') as f:
            data = json.load(f)
        
        return cls(data['name'], data['address'], data['request'], data['subscribe'])
    

    def connect(self):
        if self.isconnected:
            logger.warning(f'Already connected to {self.name}. Connection refused.')
            return None
        self.isconnected = True
        tomop.server(self.address, self.request, self.subscribe)


    def disconnect(self):
        tomop.server(self.address, self.request, self.subscribe)
        
TOMOACQUIRE_MICROSCOPE = Microscope()