'''Initialization script for BlackBerry-Tart framework.'''

import os
import sys
from threading import current_thread

# def _setup():
#     parent = os.path.dirname(__file__)
#     try:
#         with open(os.path.join(parent, 'tart.cfg')) as f:
#             for line in f:
#                 key, _, value = line.strip().partition(':')
#                 key = key.strip()
#                 value = value.strip()
#                 if key == 'sys.path' and value not in sys.path:
#                     sys.path.append(value)
#     except IOError:
#         pass


def _install_slogger2():
    from bb import slog2
    import ctypes

    appid = os.path.basename(os.getcwd())

    buffers = (slog2.slog2_buffer_t * 1)()

    cfg = slog2.slog2_buffer_set_config_t()
    cfg.num_buffers = 1
    cfg.buffer_set_name = appid.encode('ascii', 'ignore')
    cfg.verbosity_level = slog2.SLOG2_INFO

    cfg.buffer_config[0].buffer_name = b"python"
    cfg.buffer_config[0].num_pages = 1

    rc = slog2.slog2_register(cfg, buffers, 0)
    sys.stdout.flush()

    buffer = buffers[0]

    class Redirector:
        def __init__(self):
            self.pending = b''
        def write(self, text):
            ascii = text.encode('ascii', 'ignore')
            while b'\n' in ascii:
                now, ascii = ascii.split(b'\n', 1)
                if self.pending:
                    now = self.pending + now
                    self.pending = b''
                slog2.slog2c(buffer, current_thread().ident, slog2.SLOG2_INFO, now)
            self.pending += ascii
        def flush(self):
            pass

    sys.stderr = Redirector()
    sys.stdout = Redirector()

    sys.__stdout__.flush()
    sys.__stderr__.flush()


# The following code is the main entry point for the Python code
# in a Tart application, at least if the correct command line
# arguments are provided in the MANIFEST.MF file in your .bar.
#
if __name__ == '__main__':
    _install_slogger2()
    # _setup()

    try:
        import app
        a = app.App()
        a.start()
        # we don't return until the app terminates or raises an exception

    except SystemExit:
        pass

    # TODO: rather than letting exceptions get all the way up here, it
    # would be much better to catch them around the main loop, dump
    # the traceback to stdout, and then continue processing,
    # but this is how things stood at the end of the first experimental
    # stage of Tart and nobody has improved it yet...
    # Contributions are welcome! ;-)
    except:
        sys.stdout.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()


# EOF
