'''BlackBerry-Tart support code.'''

from .core import send, wait, log
from .app import Application


def dynload(name):
    '''Load platform-specific .so file from tart/lib-dynload folder,
    using the form .../lib-dynload/{name}-'''
    import os, platform, ctypes
    TARTDIR = os.path.dirname(os.path.dirname(__file__))
    ARCH = platform.processor()[:3]
    path = os.path.join(TARTDIR, 'lib-dynload', '{}-{}.so'.format(name, ARCH))
    return ctypes.CDLL(path)


# EOF
