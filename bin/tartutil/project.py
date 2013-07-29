'''Tart project stuff.'''

import os
import sys
import configparser

from .decorators import cached_property


#------------------------------------------------
#
class Project:
    ININAME = 'tart-project.ini'       # found in current or ancestor folder
    DEFSECTION = 'project'

    def __init__(self, path):
        self.root = self.get_root(path)


    def __repr__(self):
        return '<Project %s>' % self.root


    @cached_property
    def ini(self):
        '''Read Tart configuration (ini) file.'''
        ini = configparser.ConfigParser()
        ini.read(os.path.join(self.root, self.ININAME))
        return ini


    @cached_property
    def name(self):
        '''Discover name of project.'''
        name = self.config('name')
        if not name:
            name = os.path.basename(self.root)
            # print('using folder for app name (add name: to project file to avoid this)')
        return name


    def get_root(self, startpath):
        '''Search for a Tart project (ini) file.'''
        folder = os.path.normpath(startpath)
        while folder != os.path.dirname(folder):
            if os.path.isfile(os.path.join(folder, self.ININAME)):
                return os.path.abspath(folder)

            folder = os.path.dirname(folder)

        raise ValueError('file not found: {}'.format(self.ININAME))


    def config(self, name, default=None):
        '''Convenience routine to grab data from the default section.'''
        return self.ini.get(self.DEFSECTION, name, fallback=default)


    def relpath(self, path):
        '''Return a path relative to the location of the project ini file.'''
        return os.path.join(self.root, path)
