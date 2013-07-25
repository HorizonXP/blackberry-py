#!/usr/bin/env python

import sys
import os
import argparse
import importlib

# define here just in case we find a reason to change it, so we don't have
# to do a messy global replace
NAME = 'tart'


def help():
    parser.print_help()


def main():
    global parser
    parser = argparse.ArgumentParser(prog=NAME)
    parser.add_argument('-q', '--quiet', action='store_true',
        help='silence all non-critical output')
    parser.add_argument('cmd', nargs='?',
        help='subcommand')
    parser.add_argument('rest', nargs=argparse.REMAINDER, metavar='...',
        help='rest of arguments')

    global args
    args = parser.parse_args()

    if not args.cmd:
        help()
    else:
        try:
            modname = __package__ + '.commands.' + args.cmd
            mod = importlib.import_module(modname)
        except ImportError:
            # TODO: fix ugliness
            path = os.path.join(os.path.dirname(__file__), 'commands/' + args.cmd + '.py')
            if not os.path.exists(path):
                print('{}: unknown command "{}"'.format(NAME, args.cmd))
            else:
                raise
        else:
            cmd = mod.Command(args)
            cmd._run()


if __name__ == '__main__':
    main()
