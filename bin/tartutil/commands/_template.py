'''Description of command (used if class has no doc-string).'''

from .. import command


class Command(command.Command):
    '''Description of command.'''

    def add_arguments(self, parser):
        '''Add arguments for this command to an argparse.ArgumentParser.'''
        parser.add_argument('-n', nargs='?', default='none',
            help='some value (optional, default: %(default)s)')
        parser.add_argument('-x', '--extra',
            help='description of this argument')
        parser.add_argument('others', nargs='*',
            help='list of additional arguments')


    def run(self, args):
        print('arguments:')
        print('    ' + '\n    '.join(
            '{:8} = {!r}'.format(*x) for x in vars(args).items()))
