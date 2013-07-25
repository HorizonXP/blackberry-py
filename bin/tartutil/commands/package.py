'''Package an app for release or debug.'''

import sys
import os
import configparser
import datetime as dt
import errno
import marshal
import modulefinder
import subprocess
import struct
import tempfile
from py_compile import MAGIC, PyCompileError

from .. import command, project
from ..core import tart


BAR_TEMPLATE = os.path.join(os.path.dirname(__file__), 'bar-descriptor-template.xml')


def compile(codestring, filepath, timestamp, builtin_compile=compile):
    '''Byte-compile one source file to Python bytecode.'''
    try:
        codeobject = builtin_compile(codestring, filepath, 'exec', dont_inherit=True)
    except Exception as err:
        py_exc = PyCompileError(err.__class__, err.args, filepath)
        raise py_exc

    return (MAGIC
        + struct.pack('<L', int(timestamp))
        + marshal.dumps(codeobject)
        )



class Command(command.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbose = True


    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', default='release', metavar='MODE',
            choices=['release', 'debug', 'quick'],
            help='%(choices)s (default: %(default)s)')
        parser.add_argument('--arch', default='arm', metavar='ARCH',
            choices=['arm', 'x86'],
            help='platform to target (default: %(default)s)')
        parser.add_argument('-d', '--devMode', action='store_true',
            help='force -devMode (in release mode)')
        parser.add_argument('project', default='.', nargs='?',
            help='path to project (default: current directory)')


    def run(self, args):
        print('release', args)

        if args.mode == 'release' and args.arch == 'x86':
            sys.exit('release mode not currently supported on the simulator')

        self.project = project.Project(args.project)
        print('project', self.project)

        print(BAR_TEMPLATE)

        class Bag(object): pass
        config = Bag()

        appname = self.project.config('name')

        if args.mode == 'release':
            devMode = args.devMode
            config.name = appname
        else:
            config.name = '-' + appname + '-'
            devMode = True

        if args.mode == 'release':
            config.configuration = 'Device-Release'
        elif args.mode in {'debug', 'quick'}:
            device = 'Device' if args.arch == 'arm' else 'Simulator'
            config.configuration = device + '-Debug'

        config.debugtoken = os.path.join(tart.root, tart.config('debugtoken'))
        config.iconfile = self.project.config('icon')
        config.tart = tart.relpath('tart')

        config.id = self.project.config('id')
        config.version = self.project.config('version', '0.0.1')

        config.buildId = '_buildId'

        config.desc = self.project.config('description',
            'The {} app'.format(appname))

        config.theme = self.project.config('theme', 'dark')

        splashes = [x.strip() for x in self.project.config('splash', '').split()]
        print('splashes', splashes)
        config.splashscreens = '\n'.join('<image>%s</image>' % x for x in splashes)

        perms = [x.strip() for x in self.project.config('permissions', '').split()]
        if args.mode == 'quick':
            perms.append('access_shared')    # it's okay to add this twice
        print('permissions', perms)
        config.permissions = '\n'.join('<permission>%s</permission>' % x for x in perms)

        iconpath = self.project.relpath(config.iconfile)

        if not os.path.exists(iconpath):
            print('override iconfile with default')
            config.iconfile = 'blackberry-tablet-default-icon.png'
            iconpath = None

        pkgname = appname.replace(' ', '') + '.bar'

        with open(BAR_TEMPLATE) as ftemplate:
            bardesc = ftemplate.read().format(cfg=config)

        include = set()

        if args.mode != 'quick':
            # these are always included
            include.add((os.path.join(config.tart, 'js'), 'tart.js'))
            # This is actually found by find_modules, as our __main__
            # include.append((os.path.join(config.tart, 'python'), 'blackberry_tart.py'))

            assets = [x.strip() for x in self.project.config('assets', '').split()]
            for asset in assets:
                print('asset', asset)
                if os.path.isfile(asset):
                    # print('adding', asset)
                    include.add((self.project.root, asset))
                    continue

                for base, dirs, files in os.walk(self.project.relpath(asset)):
                    if '__pycache__' in dirs:
                        dirs.remove('__pycache__')

                    for f in files:
                        # temporary measure
                        if f == '.assets.index':
                            continue

                        # temporary measure?
                        if f.endswith('.pyc'):
                            continue

                        # temporary measure? this is to avoid including
                        # things like tests/ folders that aren't actually
                        # needed in the code (if they're not imported)
                        # but it also prevents a user from explicitly
                        # including any such files...
                        if f.endswith('.py'):
                            continue

                        path = os.path.join(base, f)
                        # print('adding', path)
                        relpath = os.path.relpath(path, self.project.root)
                        include.add((self.project.root, relpath))


            include.update(self.find_modules(config.tart))

        # print('include')
        # print('\n'.join('%s  %s' % x for x in sorted(include)))

        cmd = ['blackberry-nativepackager']
        with tempfile.TemporaryDirectory(prefix='tart-', dir='.') as tdir:
            os.chdir(tdir)
            try:
                with open('bar-descriptor.xml', 'w') as fbar:
                    fbar.write(bardesc)

                command = ['blackberry-nativepackager']

                def opt(*args):
                    command.extend(args)

                opt('-package', pkgname)

                if devMode:
                    opt('-devMode')

                opt('-configuration', config.configuration)

                opt('-env', 'PYTHONDONTWRITEBYTECODE=1')
                if args.mode == 'quick':
                    opt('-env', 'PYTHONPATH=shared/misc/tart/python:shared/misc/%s' % appname)
                    opt('-arg', '-qml', '-arg', 'shared/misc/%s/assets/main.qml' % appname)
                    opt('-arg', 'shared/misc/tart/python/blackberry_tart.py')

                else:
                    opt('-env', 'PYTHONPATH=app/native')
                    # TODO: allow user to specify
                    opt('-arg', '-qml', '-arg', 'app/native/assets/main.qml')
                    opt('-arg', 'app/native/blackberry_tart.pyc')

                opt('-debugToken', config.debugtoken)

                optfile = 'optfile'
                with open(optfile, 'w') as fopt:
                    def add(option):
                        print('adding', option)
                        print(option, file=fopt)

                    def addlink(base, tail):
                        print('addlink, base', base, 'tail', tail)
                        dirs = os.path.dirname(tail)
                        if dirs and not os.path.exists(dirs):
                            os.makedirs(dirs, exist_ok=True)
                        # print('os.link({!r}, {!r})'.format(os.path.join(base, tail), tail))
                        os.link(os.path.join(base, tail), tail)
                        print(tail, file=fopt)

                    add('bar-descriptor.xml')

                    if iconpath:
                        addlink(os.path.dirname(iconpath), config.iconfile)

                    if config.configuration == 'Device-Release':
                        entry = 'TartStart.so'
                    elif config.configuration == 'Device-Debug':
                        entry = 'TartStart'
                    else:
                        entry = 'TartStart-x86'

                    addlink(os.path.join(config.tart, 'entry'), entry)

                    # this is full of ugliness... we'll have to clean up
                    # the path stuff since the @optionfile approach has
                    # limitations that make this all very awkward
                    for path in splashes:
                        fullpath = os.path.dirname(self.project.relpath(path))
                        addlink(fullpath, os.path.basename(path))

                    for base, path in sorted(include):
                        if path.endswith('.py'):
                            self.compile_py(base, path)
                            add(path + 'c')

                        else:
                            addlink(base, path)

                    addlink(self.project.root, '_buildId')

                    with open('build.info', 'w') as fbuild:
                        print(dt.datetime.now(), file=fbuild)
                    add('build.info')

                opt('@' + optfile)

                # print('---------optfile')
                # os.system('type optfile')
                # os.system('copy optfile ..')
                # os.system('copy bar-descriptor.xml ..')
                # print('---------')
                # os.system('dir /s /a')
                print(' '.join(command))
                res = self.do_cmd(command)
                print(res)

                # probably too messy... find better way? (ask user?)
                if os.path.exists(pkgname):
                    dest = os.path.join('..', pkgname)
                    if os.path.exists(dest):
                        try: os.remove(dest + '.bak')
                        except OSError as ex:
                            if ex.errno != errno.ENOENT:
                                raise
                        os.rename(dest, dest + '.bak')
                    os.rename(pkgname, dest)

            finally:
                os.chdir('..')

        # import zipfile
        # import shutil
        # if os.path.exists('packaged'):
        #     shutil.rmtree('packaged')
        # os.makedirs('packaged', exist_ok=True)
        # with zipfile.ZipFile(pkgname) as fzip:
        #     print('names', fzip.namelist())
        #     fzip.extractall('packaged')


    def compile_py(self, base, path):
        fullpath = os.path.join(base, path)
        stat = os.stat(fullpath)
        with open(fullpath) as f:
            src = f.read()

        bytecode = compile(src, path, stat.st_mtime)
        parent = os.path.dirname(path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        with open(path + 'c', 'wb') as pyc:
            pyc.write(bytecode)


    def find_modules(self, tartdir):
        tartpydir = os.path.join(tartdir, 'python')
        searchpath = [tartpydir, self.project.root]
        finder = modulefinder.ModuleFinder(path=searchpath)

        finder.run_script(os.path.join(tartpydir, 'blackberry_tart.py'))

        modules = set()
        for name, mod in finder.modules.items():
            if mod.__file__ is None:
                # print('builtin:', name)
                continue

            # print('    {}'.format(name), mod.__file__)
            for base in searchpath:
                if mod.__file__.startswith(base):
                    relpath = os.path.relpath(mod.__file__, base)
                    modules.add((base, relpath))
                    break
            else:
                print('error?', mod.__file__)
            # modules.append(mod.__file__)

        # FIXME: should strip stdlib modules from here before showing
        print('Modules not found:', ', '.join(finder.badmodules))

        # FIXME: true ugliness, plus it doesn't handle x86
        if 'tart.dynload' in finder.badmodules:
            modules.add((tartpydir, 'lib-dynload/_opengl-arm.so'))

        return modules


    def do_cmd(self, cmd):
        if self.verbose:
            print('do_cmd:', cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = p.stdout.read().decode('ascii').strip()
        stderr = p.stderr.read().decode('ascii').strip()
        if stderr:
            print(stderr)
        return output

