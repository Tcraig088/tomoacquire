from tomobase.registrations.base import Item, ItemDict

class TomoacquireMicroscopes(ItemDict):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._module = 'tomoacquire'
        self._folder = 'microscopes'    
        self._hook = 'is_tomoacquire_microscope'

TOMOACQUIRE_MICROSCOPES = TomoacquireMicroscopes()
TOMOACQUIRE_MICROSCOPES.update()