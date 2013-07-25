'''Tart core stuff.'''

import os
import sys
import configparser
import re

from .decorators import cached_property


#------------------------------------------------
#
class Tart:
    TART_INI = 'tart.ini'       # found in current or ancestor folder
    STATE_DIR = '.tart-state'   # in TART_INI's folder

    def __init__(self):
        self.root = self.get_tart_root()


    @cached_property
    def statedir(self):
        '''Retrieve Tart state folder, creating if it doesn't exist.'''
        statedir = os.path.join(self.root, Tart.STATE_DIR)
        if not os.path.exists(statedir):
            os.makedirs(statedir, exist_ok=True)
        return statedir


    @cached_property
    def ini(self):
        return self.get_tart_ini()


    @staticmethod
    def get_tart_root():
        '''Search for a Tart configuration (ini) file.'''
        folder = os.path.normpath(os.getcwd())
        while folder != os.path.dirname(folder):
            if os.path.isfile(os.path.join(folder, Tart.TART_INI)):
                return folder

            folder = os.path.dirname(folder)

        raise ValueError('file not found: {}'.format(Tart.TART_INI))


    @staticmethod
    def get_tart_ini():
        '''Read Tart configuration (ini) file.'''
        root = Tart.get_tart_root()
        ini = configparser.ConfigParser()
        ini.read(os.path.join(root, Tart.TART_INI))
        return ini


    CLEANPAT = '[{}]+'.format(re.escape(r'/\\.:@'))

    def get_cache_path(self, name, folder=''):
        '''Retrieve a normalized cache file name, consisting
        of the normalized path converted to strip many special chars but
        in a way we don't think should lead to collisions.'''
        name = os.path.normpath(name)
        cleaned = re.sub(self.CLEANPAT, '_', name)

        cachedir = os.path.join(self.statedir, folder)
        if not os.path.exists(cachedir):
            os.makedirs(cachedir, exist_ok=True)

        return os.path.join(cachedir, cleaned)


    def config(self, name, default=None):
        return self.ini.get('environment', name, fallback=default)


    def relpath(self, path):
        '''Return a path relative to the location of the tart.ini file.'''
        return os.path.join(self.root, path)


tart = Tart()


