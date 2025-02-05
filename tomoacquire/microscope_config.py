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
    print(path)
    return path


def get_names():
    try:
        with open(get_path(), 'r') as f:
            microscopes = pd.read_json(f)
        return microscopes['name']  
    except:
        return []

def add_microscope(name, address, port, type, magnifications, detectors):
    try:
        with open(get_path(), 'r') as f:
            microscopes = pd.read_json(f)  
    except:
        microscopes = pd.DataFrame(columns=['name', 'address', 'port', 'type', 'detectors', 'magnifications'])

    row = pd.DataFrame({'name': name, 'address': address, 'port': port, 'type': type, 'magnifications': magnifications, 'detectors': detectors}, index=[0])
    microscopes = pd.concat([microscopes, row], ignore_index=True)

    with open(get_path(), 'w') as f:
        microscopes.to_json(f)

def get_types():
    return TOMOACQUIRE_MICROSCOPES.keys()

def get_microscope(name):
    with open(get_path(), 'r') as f:
        microscopes = pd.read_json(f)
    microscope = microscopes[microscopes['name'] == name]

    if microscope.empty:
        raise ValueError(f"Microscope with name {name} not found")

    microscope_type = microscope['type'].iloc[0]
    microscope_address = microscope['address'].iloc[0]
    microscope_port = microscope['port'].iloc[0]
    magnifications = microscope['magnifications'].iloc[0]

    print(microscope)
    print(microscope_type)
    mclass = TOMOACQUIRE_MICROSCOPES[microscope_type].controller
    return mclass(microscope_address, microscope_port, magnifications)
