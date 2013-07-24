'''Implements "help" subcommand for Tart command-line utility.'''

from .. import command


class Command(command.Command):
    def add_arguments(self, parser):
        parser.add_argument('topic', nargs='?',
            help='topic or command on which to display help')


    def run(self, args):
        if args.topic:
            import importlib
            try:
                mod = importlib.import_module(__package__ + '.' + args.topic)
            except ImportError:
                print('topic/command not found:', args.topic)
            else:
                print(mod.Command.__doc__ or mod.__doc__)
                print()

                cmd = mod.Command()
                cmd.print_help()

        else:
            import __main__ as m
            m.help()
