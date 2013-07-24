#!/usr/bin/env python
'''Package up files for a Tart binary distribution.'''

import sys
import os
import argparse
import errno
import hashlib
import subprocess
import tempfile
import zipfile


PYDIR = 'Python-3.2.2'
PYINC = 'Include'
PYCONFIG = os.path.join(PYINC, 'pyconfig.h')
LIBDIR = 'libs'
EXCLUDE = ['tart/tart-libs']
PKGPREFIX = 'tart-'


class Packager:
    def __init__(self, args):
        self.args = args
        self.exclude = [os.path.normpath(x) for x in EXCLUDE]


    def warning(self, msg):
        '''Print a warning to stderr and fail unless --force was used.'''
        if not self.args.force:
            msg += ' Use --force option.'
        print('Warning: ' + msg, file=sys.stderr)
        if not self.args.force:
            sys.exit(1)


    def error(self, msg):
        '''Print an error message to stderr and fail.'''
        print('Error: ' + msg, file=sys.stderr)
        sys.exit(2)


    def chdir(self, folder):
        if self.args.verbose:
            print('chdir:', folder)
        os.chdir(folder)


    def do_cmd(self, cmd):
        if self.args.verbose:
            print('do_cmd:', cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.stdout.read().decode('ascii').strip()
        # print(repr(output))
        return output


    def check_env(self):
        '''Check the build environment for required pieces.'''
        try:
            self.hgroot = self.do_cmd('hg root')
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                sys.exit('Mercurial (hg) not found')
            raise

        self.pydir = self.args.python or os.path.join(self.hgroot, PYDIR)
        if not os.path.isdir(self.pydir):
            self.error('Python source folder not found: ' + self.pydir)

        pyconfig = os.path.join(self.pydir, PYCONFIG)
        if not os.path.isfile(pyconfig):
            self.error('pyconfig.h not found: ' + pyconfig)

        self.libdir = self.args.libs or os.path.join(self.hgroot, LIBDIR)
        if not os.path.isdir(self.libdir):
            self.error('libs folder not found: ' + self.libdir)


    def make_archive(self, rootpath):
        '''Create archive folder from specified repo root.'''
        if ' ' in rootpath:
            rootpath = '"{}"'.format(rootpath)
        cmd = 'hg -R {} archive -r {} .'.format(
            rootpath,
            self.args.rev)
        self.do_cmd(cmd)


    def create_links(self, source, dest):
        '''Make hard links to build dependencies to resolve Makefile paths.'''
        # print('make base dir', dest)
        os.makedirs(dest, exist_ok=True)

        for base, dirs, files in os.walk(source):
            # print('base', base, 'dirs', dirs)
            relbase = os.path.relpath(base, source)
            # print('relbase', relbase)
            for d in dirs:
                path = os.path.join(dest, relbase, d)
                # print('makedir', path)
                os.makedirs(path)

            for f in files:
                # print(dest, base, f)
                path = os.path.join(dest, relbase, f)
                # print('make link', path)
                os.link(os.path.join(base, f), path)


    def build_from_archive(self):
        '''Extract specified rev/tag into archive folder and build.'''
        hgid = self.do_cmd('hg id -it -r ' + self.args.rev)
        if not hgid:
            self.error('tag or revision not found: ' + self.args.rev)

        try:
            self.revid, self.revtag = hgid.split(None, 1)
            if self.revtag == 'tip':
                raise ValueError    # hack to enter exception handler
        except ValueError:
            hgid = self.do_cmd('hg id -in -r ' + self.args.rev)
            self.revid, self.revtag = hgid.split(None, 1)

        if self.args.verbose:
            print('hg id=' + self.revid, 'tag=' + self.revtag)

        with tempfile.TemporaryDirectory(dir='.') as tempdir:
            self.chdir(tempdir)
            try:
                self.make_archive(self.hgroot)
                self.create_links(os.path.join(self.pydir, PYINC), os.path.join(PYDIR, PYINC))
                self.create_links(self.libdir, LIBDIR)
                self.build()

            finally:
                self.chdir(self.origdir)


    def build(self):
        if '+' in self.revid:
            self.warning('working copy has uncommitted changes!')

        builddir = os.getcwd()

        self.chdir('TartStart')
        try:
            self.do_cmd('make clean')    # redundant for archive builds
            self.do_cmd('make all')
            self.do_cmd('make install')
            self.do_cmd('make clean')    # redundant for archive builds
        finally:
            self.chdir(builddir)

        self.chdir('tart/tart-libs')
        try:
            self.do_cmd('make clean')    # redundant for archive builds
            self.do_cmd('make')
            self.do_cmd('make clean')    # redundant for archive builds
        finally:
            self.chdir(builddir)

        if self.revtag.startswith(PKGPREFIX):
            name = self.revtag
        else:
            name = PKGPREFIX + self.revtag + '-' + self.revid

        if self.args.verbose:
            print('building package', name)
        self.package(name)


    def is_excluded(self, path):
        path = os.path.normpath(path)
        for test in self.exclude:
            if path.startswith(test):
                if self.args.verbose:
                    print('excluding', path)
                return True
        return False


    def package(self, name):
        pkgpath = os.path.join(self.origdir, name + '.zip')

        with zipfile.ZipFile(pkgpath, 'w') as pkg:
            pkg.writestr('tart/tart.hgid', name)

            for base, dirs, files in os.walk('tart'):
                if self.is_excluded(base):
                    continue

                for f in files:
                    path = os.path.join(base, f)
                    exclude = False
                    if self.is_excluded(path):
                        continue

                    # print('adding', path)
                    pkg.write(path)

        print('created package', pkgpath)


    def run(self):
        self.origdir = os.getcwd()
        self.check_env()
        self.build_from_archive()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--python', metavar='PATH',
        help='specify path to Python source folder')
    parser.add_argument('--libs', metavar='PATH',
        help='specify path to libs folder')
    parser.add_argument('-f', '--force', action='store_true',
        help='force operation despite warnings')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='output detailed messages while running')
    parser.add_argument('rev',
        help='specify repository revision or tag to package')

    args = parser.parse_args()

    packager = Packager(args)
    packager.run()

