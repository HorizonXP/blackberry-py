'''Generate template for a new app in a folder.'''

import sys
import os
import re

from .. import command

from ..core import tart
from ..project import Project


class Command(command.Command):
    def add_arguments(self, parser):
        '''Add arguments for this command to an argparse.ArgumentParser.'''
        parser.add_argument('name',
            help='name of folder and app')
        parser.add_argument('-d', '--dir',
            help='directory in which to make app (default: new subfolder)')
        parser.add_argument('-t', '--title',
            help='title for app (default: same as name)')
        parser.add_argument('-i', '--id',
            help='id for app, e.g. com.example.Foo (default: idbase from tart.ini plus name)')


    def run(self, args):
        if not args.dir:
            args.dir = args.name

        if not args.title:
            args.title = args.name

        if not args.id:
            idbase = tart.config('idbase')
            if not idbase:
                sys.exit('Error: must specify --id or set idbase in tart.ini')
            args.id = idbase.rstrip('.') + '.' + args.name

        if not os.path.isdir(args.dir):
            print('creating new folder', args.dir)
            os.makedirs(args.dir, exist_ok=True)
        elif os.path.exists(os.path.join(args.dir, Project.ININAME)):
            sys.exit('Error: folder already contains a project file.')
        else:
            print('using existing folder', args.dir)

        config = {
            'name': args.name,
            'id': args.id,
            'title': args.title,
        }

        def replacer(match):
            text = match.group(1)
            return config.get(text, text)

        template_dir = os.path.join(os.path.dirname(__file__), 'app-template')
        for base, dirs, files in os.walk(template_dir):
            destdir = os.path.join(args.dir, os.path.relpath(base, template_dir))
            os.makedirs(destdir, exist_ok=True)
            for f in files:
                destpath = os.path.join(destdir, f)

                # Need to consider how to handle binary vs. text files,
                # assuming we'll ever have binaries.  For now, if it has
                # a 0 byte in it we don't try text substitution and otherwise
                # we blindly decode as ASCII, do substitution, and encode
                # back to ASCII, which might be totally silly. Safe for now
                # since we also know exactly what files are in our template dir.
                with open(os.path.join(base, f), 'rb') as f:
                    data = f.read()
                    if b'\0' not in data:
                        data = data.decode('ascii')
                        data = re.sub(r'<<([a-zA-Z0-9_]+)>>', replacer, data)
                        data = data.encode('ascii')

                with open(destpath, 'wb') as f:
                    f.write(data)

        print('App ready in', args.dir)
        print('Use "tart package {}" to build.'.format(args.dir))
