import zmq
import time
import numpy as np
import coolname
from tomobase.log import logger
from tomoacquire.hooks import protocol_hook
from tomoacquire.microscopes import save_microscope
import enum
from threading import Thread

class State(enum.Enum):
    IDLE = 0
    CONNECTED = 2
    SCANNING = 4

class ZMQManager():
    def __init__(self, address:str="localhost", request:int=50000, subscribe:int=50001):
        self.state = State.IDLE
        self._active_sockets = 0
        self.context = zmq.Context()
        self.request_socket = self.context.socket(zmq.REQ, 5000)
        self.subscribe_socket = self.context.socket(zmq.SUB)

        self.request_address = f"tcp://{address}:{request}"
        self.subscribe_address= f"tcp://{address}:{subscribe}"

    def connect(self):
        self.request_socket.connect(self.request_address)
        self.subscribe_socket.connect(self.subscribe_address)
        
        msg = {'id': 'connect_request'}
        reply = self.req_send(msg)
        self._active_sockets += 1

        subscribe_thread = Thread(target=self.subscribe, daemon=True)
        subscribe_thread.start()

        start = time.time()
        while (time.time() - start < 10) and self._active_sockets < 2:
            pass

        msg = {'id': 'connect_confirm'}
        reply = self.req_send(msg)
        self.State = State.CONNECTED

    def reply_recv(self):
        """Receive a message from the request socket and provides an error on timeout in case of hanging."""
        try:
            msg = self.request_socket.recv_json()
        except zmq.Again as e:
            logger.error(f"Failed to receive message: {e}")
            self.disconnect()
        return msg



class Stage(ZMQManager):
    def __init__(self,address, request, reply):
        super().__init__()

        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.tilt = 0.0
        self.defocus = 0.0

    def getstage(self):
        """get the current stage position"""
        msg = {'id': 'postion_request'}
        reply = self.req_send(msg)

        return reply
    
    @magicgui(autocall=True, call_button=False)
    def setstage(x:float, y:float, z:float, tilt:float):
        """Move the stage to the specified position."""
        msg = {'id': 'move_request'}

        msg['x'] = x
        msg['y'] = y
        msg['z'] = z
        msg['tilt'] = tilt

        for key, value in msg.items():
            if value is None:
                msg.pop(key)

        reply = self.req_send(msg)
        logger.debug(f"Stage move: {reply}")
        return reply
    

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

    

@protocol_hook(name="Request Subscribe")
class RequestSubscribeProtocol(ZMQManager):
    def __init__(self, address:str="192.168.0.1", request:int=50000, subscribe:int=50001):
        super().__init__(address, request, subscribe)

    @magicgui(call_button="Create Microscope")
    @classmethod
    def new(cls, address:str="localhost",request:int=50000, subscribe:int=50001, save:bool=False, save_as:str='New Microscope'):
        """Create a new instance of the RequestSubscribeProtocol."""
        if save:
            if name is 'New Microscope':
                name = coolname.generate_slug(2)
            else:
                name = save_as
            save_microscope(name, cls.__name__, address, request, subscribe)
        return cls(address, request, subscribe)
    
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
      



