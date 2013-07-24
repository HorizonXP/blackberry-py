'''Abstract base class for all subcommands.'''

import argparse


class Command:
    '''Specify a doc-string in subclasses to use for general help info.'''

    def __init__(self, tartargs=None):
        '''Create and initialize a new Command object.'''
        self.tartargs = tartargs
        pkg, self.name = self.__class__.__module__.rsplit('.', 1)

        from __main__ import NAME
        self.parser = argparse.ArgumentParser(prog=NAME + ' ' + self.name)

        self.add_arguments(self.parser)


    def add_arguments(self, parser):
        '''Add arguments to an argument parser.'''
        return


    def print_help(self):
        self.parser.print_help()


    def _run(self):
        '''Entry point for all commands.'''
        args = self.parser.parse_args(self.tartargs.rest)

        self.run(args)


    def run(self, args):
        '''Execute the subcommand.'''
        raise NotImplementedError
