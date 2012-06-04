#!/usr/bin/env python

import sys, os, re
import glob, tarfile, bz2
import tempfile

# used as root of output tree
TARBASE = 'blackberry-py/'


class Add(object):
    def __init__(self, src, **kwargs):
        self.src = src
        self.kwargs = kwargs
        self.tempfiles = []

    def process(self, pkg, stage):
        src = os.path.join(stage, self.src)
        # print 'globbing', src
        for self.srcpath in glob.glob(src):
            # discard symlinks
            if os.path.islink(self.srcpath):
                # print 'ignore (symlink)', self.srcpath
                continue
            else:
                # print 'process', self.srcpath
                pass
            self.outpath = os.path.relpath(self.srcpath, stage)
            # print 'outpath is now', self.outpath
            self.apply_steps()
            print 'add', self.srcpath, '-->', self.outpath
            self.package(pkg)

        self.cleanup()

    def package(self, pkg):
        pkg.add(self.srcpath, self.outpath)

    def cleanup(self):
        for f in self.tempfiles:
            os.remove(f)


    def apply_steps(self):
        for step in self.steps:
            step(self)

    def output_name(self):
        '''generate output name for file'''
        dirname, basename = os.path.split(self.outpath)
        dest = self.kwargs.get('dest', dirname)
        self.outpath = os.path.join(TARBASE, dest, basename)

    steps = [output_name]



class Library(Add):
    def output_name(self):
        # print 'find soname for', self.path
        data = os.popen('readelf -d {}'.format(self.srcpath)).read()
        soname = re.search('Library soname: \[([^]]+)\]', data).group(1)
        dirname, basename = os.path.split(self.outpath)
        dest = self.kwargs.get('dest', dirname)
        self.outpath = os.path.join(TARBASE, dest, soname)

    def maybe_strip(self):
        if not self.kwargs.get('strip'):
            return
        tname = tempfile.mktemp()
        os.system('ntoarm-strip -s -o {} {}'.format(tname, self.srcpath))
        self.srcpath = tname
        self.tempfiles.append(tname)


    steps = [output_name, maybe_strip]



def get_pyside_specs():
    return [
        Add('lib/python3.2/site-packages/PySide/__init__.py', dest='PySide/'),
        Library('lib/python3.2/site-packages/PySide/*.so', dest='PySide/', strip=True),
        Library('lib/*.so*', strip=True),
        ]

def get_qt_specs():
    return [
        Library('lib/*.so*'),
        Add('imports/Qt/'),
        Add('plugins/sqldrivers'),
        Add('plugins/platforms/libblackberry.so'),
        Add('plugins/imageformats/libqjpeg.so'),
        Add('plugins/imageformats/libqsvg.so'),
        ]


def main():
    pkg = tarfile.open('blackberry-py-{}.tar.bz2'.format(args.mode), 'w:bz2')
    try:
        for stage in ['qt', 'pyside']:
            stagedir = getattr(args, stage)
            # print 'stage dir', stagedir
            get_specs = globals()['get_{}_specs'.format(stage)]
            for spec in get_specs():
                # print '=' * 40
                spec.process(pkg, stagedir)

    finally:
        pkg.close()



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Prepare BlackBerry PySide package.')
    parser.add_argument('qt', type=str,
        help='location of Qt "stage" folder')
    parser.add_argument('pyside', type=str,
        help='location of PySide "stage" folder')
    parser.add_argument('-m', '--mode', type=str, default='full', nargs='?')

    # note: this is global:
    args = parser.parse_args()
    if args.mode not in {'lite', 'full'}:
        sys.exit('mode must be either "lite" or "full"')

    main()

