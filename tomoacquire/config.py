import json
import pandas as pd
from tomoacquire.registrations import TOMOACQUIRE_MICROSCOPES
import importlib
import inspect
import os

#path into tomoacquire module
def get_path():
    spec = importlib.util.find_spec('tomoacquire')
    if spec is None or spec.origin is None:
        raise ImportError("Cannot find the 'tomoacquire' package")

        # Construct the path to the 'tiltseries' folder within the 'plugins' folder
    path = os.path.dirname(spec.origin)
    filename = 'microscopes.json'
    path = os.path.join(path, filename)
    return path


def get_names():
    try:
        with open(get_path(), 'r') as f:
            microscopes = pd.read_json(f)
            return microscopes['name'].to_list()
    except:
        return []
 
def add_microscope(**kwargs):
    names = get_names()
    if kwargs['name'] in names:
        raise ValueError(f"Microscope with name {kwargs['name']} already exists")
    
    name = kwargs['name']
    address = kwargs['address']
    port = kwargs['port']
    classification = kwargs['classification']
    magnifications = kwargs['magnifications']
    detectors = kwargs['detectors']
    detector_pixelsize = kwargs['detector_pixelsize']
    
    if not os.path.exists(get_path()):
        with open(get_path(), 'w') as f:
            pass
        microscopes = pd.DataFrame(columns=['name', 'address', 'port', 'classification', 'magnifications', 'detectors', 'detector_pixelsize'])
    
    try:
        with open(get_path(), 'r') as f:
            microscopes = pd.read_json(f)  
    except:
        microscopes = pd.DataFrame(columns=['name', 'address', 'port', 'classification', 'magnifications', 'detectors', 'detector_pixelsize'])

    row = pd.DataFrame([[name, address, port, classification, magnifications, detectors, detector_pixelsize]], columns=['name', 'address', 'port', 'classification', 'magnifications', 'detectors', 'detector_pixelsize'])
    microscopes = pd.concat([microscopes, row], ignore_index=True)

    with open(get_path(), 'w') as f:
        microscopes.to_json(f)

def get_microscope(name):
    with open(get_path(), 'r') as f:
        microscopes = pd.read_json(f)
        
    microscope = microscopes[microscopes['name'] == name]
    if microscope.empty:
        raise ValueError(f"Microscope with name {name} not found")
    microscope = microscope.iloc[0]
    classification = microscope['classification']
    address = microscope['address']
    port = microscope['port']
    magnifications = microscope['magnifications']
    detectors = microscope['detectors']
    detector_pixelsize = microscope['detector_pixelsize']

    mclass = TOMOACQUIRE_MICROSCOPES[classification].value
    return mclass(address, port, magnifications, detectors, detector_pixelsize)
