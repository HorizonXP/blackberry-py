'''BlackBerry-Tart support code.'''

import json

import _tart


def send(type, **kwargs):
    '''Call from Python as tart.send(type, ...) with any keyword
    arguments you want packaged up to send to JavaScript.
    See also the implementation of Tart._onMessage in the tart.js file.
    '''
    _tart.send(json.dumps([type, kwargs]))


def wait():
    '''Main call for the main Python thread to implement the required
    Tart event loop.  Blocks until new messages arrive from JavaScript,
    or until the Cascades Application is shutting down at which point
    the _tart.wait() call will raise a SystemExit exception, which must
    not be completely swallowed.  (That is, if you want to catch it
    to do some processing on the way out, that's fine, but make sure you
    re-raise it when you're done, and keep the processing short.)
    '''
    data = _tart.wait()
    try:
        msg = json.loads(data)
    except ValueError:
        msg = {}
    return msg


# TODO: remove this, and just have people call print()?  Or
# plug it into the standard Python logging module instead?
# Contributions are welcome.
def log(*args):
    '''Relies on the slogger2 configuration to send this to the right place.
    See blackberry_tart.py and its _install_slogger2().
    '''
    print(*args)



# EOF
