import ctypes
from ctypes import c_int, c_void_p, c_uint, POINTER, Structure

BPS_VERSION = 1000000
BPS_VERSION_STRING = "1.0.0"

BPS_SUCCESS = 0
BPS_FAILURE = -1

#~ from lib_builder import funcdef
class _LibWrapper:
    def __init__(self, libname):
        self.lib = ctypes.CDLL(libname)

    def func(self, name, info):
        argtypes, restype = info
        func = getattr(self.lib, name)
        func.argtypes, func.restype = info
        return func


class bps_event_t(Structure):
    _fields_ = []
#~ bps_event_t_p = POINTER(bps_event_t)


_bps = _LibWrapper('libbps.so.2')
for _name, _info in [
    # int bps_get_version(void);
    ('bps_get_version', ([], c_int)),

    # int bps_initialize(void);
    ('bps_initialize', ([], c_int)),

    # void bps_shutdown(void);
    ('bps_shutdown', ([], None)),   # maybe can't do restype = None

    # int bps_get_event(bps_event_t **event, int timeout_ms);
    ('bps_get_event', ([POINTER(POINTER(bps_event_t)), c_int], c_int)),

    # int bps_push_event(bps_event_t *event);
    ('bps_push_event', ([POINTER(bps_event_t)], c_int)),

    # int bps_register_domain(void);
    ('bps_register_domain', ([], c_int)),

    # void bps_set_verbosity(unsigned verbosity);
    ('bps_set_verbosity', ([c_uint], None)),   # maybe can't do restype = None

    # void bps_free(void *ptr);
    ('bps_free', ([c_void_p], None)),   # maybe can't do restype = None
    ]:
    globals()[_name] = _bps.func(_name, _info)
