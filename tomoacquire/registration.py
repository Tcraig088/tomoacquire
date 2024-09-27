

class TiltSchemeRegister():
    _instance =None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TiltSchemeRegister, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._tiltscheme = None
        