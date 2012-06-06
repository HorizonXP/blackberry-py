import os
import sys

BBPYPATH = os.path.dirname(os.path.dirname(__file__))

if sys.platform == 'qnx6':
    os.environ['LD_LIBRARY_PATH'] = os.path.join(BBPYPATH, 'lib')
    os.environ['QT_PLUGIN_PATH'] = os.path.join(BBPYPATH, 'plugins')
    os.environ['QML_IMPORT_PATH'] = os.path.join(BBPYPATH, 'imports')
    os.environ['QT_QPA_PLATFORM'] = 'blackberry'

    # from pprint import pprint
    # pprint(dict(os.environ))

from .app import Application

# launch telnet-based command line interface (CLI)
if '--cli' in sys.argv:
    try:
        from . import cli
    except ImportError:
        print('unable to import cli, ignoring --cli option', file=sys.stderr)
    else:
        import threading
        t = threading.Thread(target=cli.run)
        t.daemon = True
        t.start()


__all__ = ['Application']
