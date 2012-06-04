import os

BBPYPATH = os.path.dirname(os.path.dirname(__file__))

os.environ['LD_LIBRARY_PATH'] = os.path.join(BBPYPATH, 'lib')
os.environ['QT_PLUGIN_PATH'] = os.path.join(BBPYPATH, 'plugins')
os.environ['QML_IMPORT_PATH'] = os.path.join(BBPYPATH, 'imports')
os.environ['QT_QPA_PLATFORM'] = 'blackberry'

from .app import Application

__all__ = ['Application']
