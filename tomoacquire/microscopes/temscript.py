import zmq
import numpy as np
from tomobase.log import logger
from tomoacquire.hooks import tomoacquire_hook
import enum
from threading import Thread

class State(enum.Enum):
    IDLE = 0
    CONNECTED = 2
    SCANNING = 4


class Stage:
    def __init__(self,x:float=0.0, y:float=0.0, z:float=0.0, tilt:float=0.0):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.tilt = 0.0
        self.defocus = 0.0

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
class TEMScriptMicroscope():
    def __init__(self, address:str="192.168.0.1", request:int=50000, subscribe:int=50001):
        self.state = State.IDLE
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

        receive_thread = Thread(target=self.receive_data, daemon=True)
        receive_thread.start()

    def connect(self):
        msg = {'id': 'connect_request'}
        self.request_socket.send_json(msg)
        reply = self.request_socket.recv_json()
        self.detector_options = reply.get('detectors', {})
        self.state = State.CONNECTED
        return reply

    def set_scan(self, isscan:bool=True, dwell_time:float=0.5, frame_size:int=1024, scan_time:float=0.63, detectors:list=[]):
        """set the scan parameters for the microscope"""

        msg = {'id': 'scan_request'}
        msg['isscan'] = isscan
        msg['dwell_time'] = dwell_time
        msg['frame_size'] = frame_size
        msg['scan_time'] = scan_time
        msg['detectors'] = detectors

        self.request_socket.send_json(msg)
        reply = self.request_socket.recv_json()
        logger.debug(f"Scan settings: {reply}")

    def start_scan(self, isscan:bool=True, start:bool=True):
        """Start or stop the scan."""
        msg = {'id': 'imaging_request'}
        msg['isscan'] = isscan
        msg['start'] = start

        self.request_socket.send_json(msg)
        reply = self.request_socket.recv_json()
        logger.debug(f"Scan start/stop: {reply}")
        if reply['success'] and start:
            self.state = State.SCANNING
        elif reply['success'] and not start:
            self.state = State.CONNECTED
        return reply

    def set_stage_positions(self, x=None, y=None, z=None, tilt=None):
        """Move the stage to the specified position."""
        msg = {'id': 'move_request'}

        msg['x'] = x
        msg['y'] = y
        msg['z'] = z
        msg['tilt'] = tilt

        for key, value in msg.items():
            if value is None:
                msg.pop(key)

        self.request_socket.send_json(msg)
        reply = self.request_socket.recv_json()
        logger.debug(f"Stage move: {reply}")

    def receive_data(self):
        poller = zmq.Poller()
        poller.register(self.subscribe_socket, zmq.POLLIN)
        # This loop can run in a thread, or you can call receive_data periodically
        while True:
            events = dict(poller.poll(timeout=100))  # 100 ms timeout, adjust as needed
            if self.subscribe_socket in events:
                msg = self.subscribe_socket.recv_json()
                logger.debug(f"Received data: {msg['shape']}")
                logger.debug(f"Received data: {msg['isscan']}")
                # emit, process, or handle msg here
      

    def get_stage_positions(self):
        """get the current stage position"""
        msg = {'id': 'postion_request'}
        self.request_socket.send_json(msg)
        reply = self.request_socket.recv_json()

        reply.pop('id')
        logger.debug(f"Stage position: {reply}")
        return reply


