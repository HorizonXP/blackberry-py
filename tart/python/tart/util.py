'''General-purpose and *simple* standalone utility routines for Tart.'''

from itertools import count
from threading import Lock


def ascii_bytes(str_or_bytes, errors='ignore'):
    '''Return input converted to ASCII-encoded bytes, whether
    it starts off as a string or a bytes.
    '''
    try:
        return str_or_bytes.encode('ascii', errors=errors)
    except AttributeError:
        return str_or_bytes


def clamp(value, min, max):
    '''Return value or, if it's beyond the min/max limits,
    return the closest limit.'''
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


def counter_id(counter=count(1), lock=Lock()):
    '''Return a serial number in a thread-safe manner, for instance ids.'''
    with lock:
        return next(counter)


# EOF
