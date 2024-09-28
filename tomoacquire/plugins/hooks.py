


def tomoacquire_hook_tiltscheme(name):
    def decorator(cls):
        cls.tomoacquire_name = name
        cls.is_tomoacquire_tiltscheme = True
        return cls
    return decorator