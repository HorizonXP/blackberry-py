import ctypes

class _func:
    '''Function definition, replaced by reference to function in library
    when register_functions() is called.'''
    def __init__(self, *args):
        self.args = args


def _register_funcs(libname, namespace):
    lib = ctypes.CDLL(libname)

    for name, fdef in namespace.items():
        if isinstance(fdef, _func):
            func = getattr(lib, name)
            func.restype = fdef.args[0]
            func.argtypes = fdef.args[1:]
            namespace[name] = func
