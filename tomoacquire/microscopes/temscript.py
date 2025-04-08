
import zmq
from tomobase.log import logger
from tomoacquire.hooks import tomoacquire_hook


class Stage:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.tilt = 0.0

class Beam:
    def __init__(self):
        self.current = 0.0
        self.magnification = 0.0
        self.blanked = False


class ScanSettings:
    def __init__(self):
        self.isscan = False
        self.dwell_time = 0.0
        self.frame_size = 0
        self.scan_time = 0.0
        self.detectors = []

    

@tomoacquire_hook(name="TEMScript")
class TEMSCriptMicroscope():
    def __init__(self, address:str="192.168.0.1", request:int=50000, subscribe:int=50001):
        self.address = address
        self.request_port = request
        self.subscribe_port = subscribe

        self.context = zmq.Context()
        self.request_socket = self.context.socket(zmq.REQ)
        self.request_socket.connect(f"tcp://{self.address}:{self.request_port}")
        self.subscribe_socket = self.context.socket(zmq.SUB)
        self.subscribe_socket.connect(f"tcp://{self.address}:{self.subscribe_port}")

        self.magnification_options = []
        self.detector_options = {}

    def connect(self):
        msg = {'id': 'connect_request'}
        self.request_socket.send_json(msg)
        reply = self.request_socket.recv_json()
        return reply

    def set_scan(self, isscan:bool=True, dwell_time:float=0.5, frame_size:int=1024, scan_time:float=0.63, detectors:list=[]):
        """set the scan parameters for the microscope"""

        msg = {'id': 'scan_request'}
        msg['isscan'] = isscan
        msg['dwell_time'] = dwell_time*10**(-6)  # convert to seconds
        msg['frame_size'] = frame_size
        msg['scan_time'] = scan_time
        msg['detectors'] = detectors

        self.request_socket.send_json(msg)
        reply = self.request_socket.recv_json()
        logger.debug(f"Scan settings: {reply}")

    def move_stage(self, x:float=0.0, y:float=0.0, z:float=0.0, tilt:float=0.0):
        """move the stage to the specified position"""
        msg = {'id': 'move_request'}
        msg['x'] = x
        msg['y'] = y
        msg['z'] = z
        msg['tilt'] = tilt

        self.request_socket.send_json(msg)
        reply = self.request_socket.recv_json()
        logger.debug(f"Stage move: {reply}")



