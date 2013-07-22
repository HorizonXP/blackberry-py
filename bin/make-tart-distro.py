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


def do_cmd(cmd):
    print('do_cmd: ' + cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = p.stdout.read().decode('ascii').strip()
    # print(repr(output))
    return output


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


    def check_env(self):
        '''Check the build environment for required pieces.'''
        try:
            self.hgroot = do_cmd('hg root')
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
            self.args.rev or self.args.tag)
        do_cmd(cmd)

        self.pkg_rev = self.args.rev or self.args.tag


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
        with tempfile.TemporaryDirectory(dir='.') as tempdir:
            os.chdir(tempdir)
            try:
                self.make_archive(self.hgroot)
                self.create_links(os.path.join(self.pydir, PYINC), os.path.join(PYDIR, PYINC))
                self.create_links(self.libdir, LIBDIR)
                self.build()

            finally:
                os.chdir(self.origdir)


    def build_from_local(self):
        hgid = do_cmd('hg id')
        self.pkg_rev, branch = hgid.split(None, 1)
        if '+' in self.pkg_rev:
            self.warning('working copy has uncommitted changes.')

        origdir = os.getcwd()
        os.chdir(self.hgroot)
        try:
            self.build()
        finally:
            if origdir:
                os.chdir(origdir)


    def build(self):
        builddir = os.getcwd()

        os.chdir('TartStart')
        try:
            # do_cmd('make clean')
            do_cmd('make all')
            do_cmd('make install')
            # do_cmd('make clean')
        finally:
            os.chdir(builddir)

        os.chdir('tart/tart-libs')
        try:
            do_cmd('make clean')
            do_cmd('make')
            do_cmd('make clean')
        finally:
            os.chdir(builddir)

        self.package()


    def is_excluded(self, path):
        path = os.path.normpath(path)
        for test in self.exclude:
            if path.startswith(test):
                print('excluding', path)
                return True
        return False


    def package(self):
        pkgname = 'tart-{}.zip'.format(self.pkg_rev)
        pkgpath = os.path.join(self.origdir, pkgname)

        with zipfile.ZipFile(pkgpath, 'w') as pkg:
            pkg.writestr('tart/tart.hgid', self.pkg_rev)

            for base, dirs, files in os.walk('tart'):
                if self.is_excluded(base):
                    continue

                for f in files:
                    path = os.path.join(base, f)
                    exclude = False
                    if self.is_excluded(path):
                        continue

                    print('adding', path)
                    pkg.write(path)

        print('created package', pkgpath)


    def run(self):
        self.origdir = os.getcwd()
        self.check_env()

        if self.args.rev or self.args.tag:
            self.build_from_archive()
        else:
            self.build_from_local()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true',
        help='force operation despite warnings')
    parser.add_argument('-r', '--rev',
        help='specify repository revision to package')
    parser.add_argument('-t', '--tag',
        help='specify repository tag to package')
    parser.add_argument('--python',
        help='specify path to Python source folder')
    parser.add_argument('--libs',
        help='specify path to libs folder')

    args = parser.parse_args()

    if args.rev and args.tag:
        sys.exit('Use only --rev or --tag, not both.')

    packager = Packager(args)
    packager.run()

