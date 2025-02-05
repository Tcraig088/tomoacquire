
def tomoacquire_hook(name: str):
    """a decorator used to mark a class as a tiltscheme. The class is either a standard class used to define the tiltscheme or a QWidget used to attach to napari. 
    see the plugins tutorial for more information on how to use this decorator. returns a decorated class

    Args:
        name (str): the name of the tilt scheme. Should be readable casing and spaces. 
    """
    def decorator(cls):
        cls.tomoacquire_name = name
        cls.is_tomoacquire_microscope = True
        return cls
    return decorator