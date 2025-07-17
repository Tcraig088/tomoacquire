from tomobase.registrations.base import Item, ItemDict

class TomoAcquireProtocol(ItemDict):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._module = 'tomoacquire'
        self._folder = 'protocols'    
        self._hook = 'is_tomoacquire_protocol'

TOMOACQUIRE_PROTOCOLS = TomoAcquireProtocol()
TOMOACQUIRE_PROTOCOLS.update()