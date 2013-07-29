'''Mirror a directory tree to another location.'''
# uses code from http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
# see also http://msdn.microsoft.com/en-us/library/windows/desktop/aa364391%28v=vs.85%29.aspx

from __future__ import print_function

import os
import sys
import argparse
import configparser
import errno
import fnmatch
import hashlib
import pickle
import queue
import re
import shutil
import signal
import stat
import textwrap
import threading
import time
from collections import OrderedDict, defaultdict, namedtuple

import win32file
import win32con

from .. import command
from ..core import tart
from ..project import Project

DEBUG = True

# our section name in config files (appears in square brackets)
CFGSECTION = 'quickdeploy'

# where we preserve files we delete from target that may not be kept by user
SAFEDIR = 'qd-safe' # in TART_DATA folder

# where we save the target folder state info to reduce latency at startup
CACHEDIR = 'qd-cache' # in TART_DATA folder

# flags valid QuickDeploy target, as protection against accidental destruction
# of data if there's a bug or wrong configuration or user error
TARGET_FLAG = 'quickdeploy-target'

# Could also just normalize everything with normpath() but I like
# seeing forward slashes everywhere including in debug output on Windows.
if os.path.sep == '/':
    fwdnormpath = os.path.normpath
else:
    def fwdnormpath(path):
        path = os.path.normpath(path)
        return path.replace(os.path.sep, '/')


FileEvent = namedtuple('FileEvent', ['timestamp', 'source', 'path'])


def log(*args, **kwargs):
    print('{:.3f}s'.format(get_time()), *args, **kwargs)


#------------------------------------------------
#
def get_time(basetime=time.time()):
    '''Return seconds since the app started. This is used for timestamps
    that are more readable than the 10-digit seconds-since-1970 variety.'''
    return time.time() - basetime



#------------------------------------------------
#
class Filter:
    DEFAULT_OUTCOME = 'include'
    CMD_RESET = 'reset'
    CMD_INCLUDE = 'include'
    CMD_EXCLUDE = 'exclude'

    def __init__(self, base, rules=[]):
        self.base = base
        self.reset()
        self.add_rules(rules)
        # print('base', self.base)


    def reset(self):
        self.default_outcome = Filter.DEFAULT_OUTCOME
        self.rules = OrderedDict()


    def add_rules(self, rules):
        if isinstance(rules, configparser.ConfigParser):
            rules = rules.get(CFGSECTION, 'filters', fallback='').strip().split('\n')

        for rule in rules:
            cmd, _, pattern = rule.partition(' ')
            if cmd == Filter.CMD_RESET:
                self.reset()
            elif cmd in {Filter.CMD_INCLUDE, Filter.CMD_EXCLUDE}:
                if not pattern:
                    self.default_outcome = cmd
                else:
                    _ = self.rules.pop(pattern, None)
                    self.rules[pattern] = cmd

        # from pprint import pprint
        # print('default', self.default_outcome)
        # pprint(self.rules)


    @staticmethod
    def iswild(path, _wild=frozenset('?*[')):
        return bool(set(path) & _wild)


    def __call__(self, path):
        # print('-' * 20)
        # print('path', path)
        _path = os.path.relpath(path, self.base)
        if _path.startswith(os.pardir):
            raise ValueError('path is outside project: ' + path)
        # print('relpath', _path)
        _path = fwdnormpath('/' + _path)
        # print('fwdnorm', _path)
        # print('final [', _path, ']')

        outcome = self.default_outcome
        used_pattern = None
        for pattern, cmd in self.rules.items():
            if outcome == cmd:  # skip rule if it wouldn't change the outcome
                continue

            # print('rule', int(Filter.iswild(pattern)), pattern, cmd)

            matched = False

            if Filter.iswild(pattern):
                if fnmatch.fnmatch(_path, pattern):
                    matched = True

            elif '/' in pattern:
                if pattern == _path:
                    matched = True
                    outcome = cmd

            elif os.path.basename(_path) == pattern:
                matched = True

            if matched:
                outcome = cmd
                used_pattern = pattern

        # if DEBUG:
        #     print('{}: {}  ({})'.format(outcome, _path, '"' + used_pattern + '"' if used_pattern else 'default'))

        if outcome == 'include':
            return path
        else:
            return None



#------------------------------------------------
#
class File:
    def __init__(self, path, stat=None):
        self.path = path
        self.stat = stat
        self.last_checked = get_time()


    @property
    def name(self):
        return os.path.basename(self.path)


    def __repr__(self):
        r = ['%s' % self.path]
        return ''.join(r)


    def read_stat(self):
        self.stat = os.stat(self.path)



#------------------------------------------------
#
class FileSet:
    def __init__(self, path, filter=None):
        self.path = fwdnormpath(path)
        self.name = os.path.basename(path)

        def unfiltered(path):
            return path

        self.filter = filter or unfiltered

        self.files = {}


    def __repr__(self):
        r = ['<FileSet %s' % self.path]
        r.append('>')
        return ''.join(r)


    def add_file(self, file):
        rel = os.path.relpath(file.path, self.path)
        self.files[rel] = file


    def populate(self):
        for base, dirs, files in os.walk(self.path):
            for name in files:
                path = os.path.join(base, name)
                path = self.filter(path)
                if not path:
                    continue

                info = os.stat(path)
                if stat.S_ISREG(info.st_mode):
                    path = fwdnormpath(path)
                    f = File(path, info)
                    self.add_file(f)
                    # print('found', f, os.path.relpath(path, self.path))

            # filter out subdirectories and update dirs so we don't traverse
            included = []
            for name in dirs:
                if self.filter(os.path.join(base, name)):
                    included.append(name)
            dirs[:] = included


    def restore_state(self):
        cachepath = tart.get_cache_path(self.path, CACHEDIR)
        try:
            with open(cachepath, 'rb') as fstate:
                try:
                    self.files = pickle.load(fstate)
                except Exception as ex:
                    print('error unpickling:', ex)
                    return False

            return True

        except IOError as ex:
            if ex.errno != errno.ENOENT:
                raise

        return False


    def save_state(self):
        cachepath = tart.get_cache_path(self.path, CACHEDIR)
        with open(cachepath, 'wb') as fstate:
            pickle.dump(self.files, fstate)


    def refresh(self):
        pass
        # print('Warning: Destination.refresh() not implemented yet')


    def dump(self):
        for path in sorted(self.files):
            print(self.files[path])



#------------------------------------------------
#
class SourceMonitor_win32:
    '''Monitor a source folder tree for changes, reporting renames
    and adds/deletes/modifies to a sink'''

    def __init__(self, source, sink=None):
        self.source = source

        def dummy_sink(*args):
            print('sink:', args)

        self.sink = sink or dummy_sink    # callback to report events


    def __repr__(self):
        return '<SourceMonitor %s>' % self.source.path


    def start(self):
        self._thread = threading.Thread(target=self._thread_run)
        self._thread.daemon = True
        self._thread.start()


    def _thread_run(self):
        FILE_LIST_DIRECTORY = 0x0001

        srcpath = self.source.path
        self.hDir = win32file.CreateFile(
            srcpath,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
            )

        if DEBUG:
            log('monitoring', os.path.basename(srcpath), 'for changes')

        try:
            while True:
                self._monitor_changes()
        finally:
            self.sink('stopped')    # signals termination
            win32file.CloseHandle(self.hDir)


    def _monitor_changes(self):
        # ReadDirectoryChangesW takes a previously-created
        # handle to a directory, a buffer size for results,
        # a flag to indicate whether to watch subtrees and
        # a filter of what changes to notify.
        #
        # NB Tim Juchcinski reports that he needed to up
        # the buffer size to be sure of picking up all
        # events when a large number of files were
        # deleted at once.
        #
        results = win32file.ReadDirectoryChangesW(
            self.hDir,
            1024,
            True,   # watch subtrees
            (  win32con.FILE_NOTIFY_CHANGE_FILE_NAME
             | win32con.FILE_NOTIFY_CHANGE_DIR_NAME
             # | win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
             # | win32con.FILE_NOTIFY_CHANGE_SIZE
             | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
             # | win32con.FILE_NOTIFY_CHANGE_SECURITY
            ),
            None,
            None
            )

        timestamp = get_time()
        for code, filepath in results:
            self.sink(FileEvent(timestamp, self.source, filepath))



#------------------------------------------------
#
class Source(FileSet):
    def __init__(self, project, sink=None):
        self.project = project

        filter = Filter(project.root)
        filter.add_rules(tart.ini)
        filter.add_rules(project.ini)

        super().__init__(project.root, filter)

        self._monitor = SourceMonitor_win32(self, sink)


    def __repr__(self):
        return '<Source %s>' % self.name


    def start(self):
        self._monitor.start()



#------------------------------------------------
#
class Destination(FileSet):
    def __init__(self, target, project):
        self.target = target
        self.project = project
        super().__init__(os.path.join(target.path, project.name))


    def __repr__(self):
        return '<Destination %s>' % self.path



#------------------------------------------------
#
class Target:
    '''Manages a target device, represented mainly as a path to a
    folder for quick deployment of apps.'''

    def __init__(self, path):
        self.path = path
        self.destinations = OrderedDict()


    def __repr__(self):
        r = ['<Target ' + self.path]
        if len(self.destinations) == 1:
            r.append(', 1 dest')
        else:
            r.append(', %s dests' % len(self.destinations))
        r.append('>')
        return ''.join(r)


    def add_destination(self, dest):
        if dest.name in self.destinations:
            raise ValueError('duplicate destination %s' % dest.name)

        self.destinations[dest.name] = dest


    def save_state(self):
        for d in self.destinations.values():
            d.save_state()


#------------------------------------------------
#
class QuickDeploy:
    def __init__(self, args):
        self.args = args
        self.queue = queue.Queue()

        self.projects = []
        self.sources = []
        self.targets = []
        self.destinations = defaultdict(list)

        self.pending = {}

        self.count = 0


    @property
    def sanctuary(self):
        try:
            self._sanctuary
        except AttributeError:
            self._sanctuary = os.path.join(tart.statedir, SAFEDIR)
        return self._sanctuary


    def safe_delete(self, destpath, preserve=False):
        '''Safely delete from destination, with preservation in the
        sanctuary folder if requested.'''
        if preserve:
            stat = os.stat(destpath)
            data = open(destpath, 'rb').read()
            if data:
                digest = self.checksum(data)

                os.makedirs(self.sanctuary, exist_ok=True)
                fname = os.path.basename(destpath) + '-' + digest
                copypath = os.path.join(self.sanctuary, fname)
                if not os.path.exists(copypath):
                    open(copypath, 'wb').write(data)
                    # TODO: log it so user can trace this
                    if DEBUG:
                        log('preserved', destpath)
                else:
                    if DEBUG:
                        log('already preserved', destpath)

            else:
                if DEBUG:
                    log('empty file, not preserving', destpath)

        os.remove(destpath)
        if DEBUG:
            log('removed', destpath)


    def checksum(self, data):
        '''Return a checksum for some data.'''
        return hashlib.md5(data).hexdigest()


    def cfg_value(self, name, fallback=''):
        '''Retrieve a value from tart.ini file's [quickdeploy] section.'''
        return tart.ini.get(CFGSECTION, name, fallback=fallback)


    def copyfile(self, src, dest, check_hash=False):
        # print('check_hash', check_hash)
        if check_hash:
            hash1 = hashlib.md5(open(src, 'rb').read()).digest()
            try:
                hash2 = hashlib.md5(open(dest, 'rb').read()).digest()
            except IOError:
                hash2 = None

            if hash1 == hash2:
                # print('skip   {}'.format(dest))
                return False

        log('copy', dest)
        try:
            shutil.copyfile(src, dest)
        except IOError as ex:
            log('Error', ex, 'copying to', dest)
            return False

        return True


    def setup(self):
        # build Projects from list in config file
        log('scan sources')
        for path in self.cfg_value('sources').strip().split():
            project = Project(os.path.join(tart.root, path))
            self.projects.append(project)

        # build Sources from projects
        for project in self.projects:
            source = Source(project, sink=self.queue.put)
            self.sources.append(source)
            source.populate()

        # build Targets from list in config file
        log('prepare destinations')
        to_refresh = []
        for path in self.cfg_value('targets').strip().split():
            target = Target(path)

            for project in self.projects:
                dest = Destination(target, project)
                target.add_destination(dest)
                self.destinations[project.name].append(dest)

                if dest.restore_state():
                    to_refresh.append(dest)
                else:
                    start = time.time()
                    log('scanning', dest.path, end=' ... ')
                    sys.stdout.flush()
                    # if dest.path == 'q:/misc/tart':
                    #     import pdb; pdb.set_trace()

                    dest.populate()
                    elapsed = time.time() - start
                    print('(%.1fs)' % elapsed)

            self.targets.append(target)

        log('targets', self.targets)
        # import pdb; pdb.set_trace()

        # activate source monitoring threads
        for source in self.sources:
            source.start()

        # activate destination refresh in background for those which were cached
        for dest in to_refresh:
            dest.refresh()


    DEFAULT_TIMEOUT = 1.0

    MIN_LATENCY = 0.25

    def calc_timeout(self):
        if not self.pending:
            return self.DEFAULT_TIMEOUT

        earliest = sorted(self.pending.values())[0].timestamp
        return max(earliest + self.MIN_LATENCY - get_time(), 0)


    def is_old_enough(self, event):
        return event.timestamp <= get_time() - self.MIN_LATENCY


    def get_old_events(self):
        # log(':: get_old_events')
        if not self.pending:
            return

        processed = []
        for event in self.pending.values():
            if self.is_old_enough(event):
                # log('now older', event)
                yield event
                processed.append(event.path)

        for path in processed:
            del self.pending[path]


    def raw_get_events(self):
        '''Retrieve events directly from incoming queue.'''
        # log(':: get_raw_events')

        quiet = False
        while True:
            try:
                timeout = self.calc_timeout()
                # if timeout != self.DEFAULT_TIMEOUT or not quiet:
                #     log('get, with timeout {:.3f}s'.format(timeout))
                event = self.queue.get(timeout=timeout)

            except queue.Empty:
                quiet = timeout == self.DEFAULT_TIMEOUT

                if self.pending:
                    for event in self.get_old_events():
                        yield event

            else:
                quiet = False
                yield event


    def get_events(self):
        # log(':: get_events')
        for event in self.raw_get_events():
            if event == 'stopped':
                continue

            # if event did not occur long enough ago, store for later
            if not self.is_old_enough(event):
                # log('store for later', event)
                # if event.path in self.pending:
                #     log('note: existing event for same path', self.pending[event.path])
                self.pending[event.path] = event

            else:
                yield event


    def presync(self, source, dest):
        '''Synchronize source and target folders.'''
        dests = set(dest.files)
        sources = set(source.files)

        to_delete = dests - sources
        to_add = sources - dests
        to_check = sources & dests

        flagpath = os.path.join(dest.target.path, TARGET_FLAG)
        if not os.path.exists(flagpath):
            print('\aError, target not flagged for quickdeploy:', dest.target.path)
            return

        if to_delete:
            text = ' '.join(sorted(to_delete))
            print('To delete:')
            print('\n'.join(textwrap.wrap(text)))

        for path in sorted(to_delete):
            dpath = fwdnormpath(dest.files[path].path)
            log('delete', dpath)
            # import pdb; pdb.set_trace()
            try:
                self.safe_delete(dpath, preserve=True)
            except OSError:
                print('Warning: unable to remove', dpath)

            if not os.path.exists(dpath):
                del dest.files[path]

        # if to_check:
        #     text = ' '.join(sorted(to_check))
        #     print('To check: everything else')
            # print('\n'.join(textwrap.wrap(text)))

        for path in sorted(to_check):
            srcfile = source.files[path]
            sstat = srcfile.stat
            ssig = sstat.st_size

            destfile = dest.files[path]
            dstat = destfile.stat
            dsig = dstat.st_size

            spath = fwdnormpath(source.files[path].path)
            dpath = fwdnormpath(dest.files[path].path)

            # log('update', dpath, dsig, ssig)
            # for now copy here only if sizes are different
            # FIXME: this won't handle the case where a file has changed
            # when we weren't running in a way that doesn't change its size!
            if ssig != dsig:
                if self.copyfile(spath, dpath):
                    destfile.read_stat()

        if to_add:
            text = ' '.join(sorted(to_add))
            print('To add:')
            print('\n'.join(textwrap.wrap(text)))

        for path in sorted(to_add):
            dpath = fwdnormpath(os.path.join(dest.path, path))
            spath = fwdnormpath(source.files[path].path)
            # print('add   ', dpath)
            parent = os.path.dirname(dpath)
            if not os.path.exists(parent):
                os.makedirs(parent)
            self.copyfile(spath, dpath, check_hash=False)
            stat = os.stat(dpath)
            # import pdb; pdb.set_trace()
            dest.add_file(File(dpath, stat))


    def process(self, event):
        self.count += 1
        log('#{} {}'.format(self.count, event))

        # note the unhandled case where a rename operation affects
        # a file where the old and the new path have a different
        # filter outcome... we'd need to convert it either into a
        # delete or an add in those cases but for now ignore it as
        # an unusual case

        source = event.source
        spath = os.path.join(source.path, event.path)

        spath = source.filter(spath)
        if not spath:
            # print('filtered out', spath)
            return

        try:
            sstat = os.stat(spath)
            source_exists = True
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                source_exists = False
            else:
                raise

        if os.path.isdir(spath) or (
                event.path in source.files
            and stat.S_ISDIR(source.files[event.path].stat.st_mode)):
            log('ignoring folder')
            return

        for dest in self.destinations[source.project.name]:
            print('update', dest)

            dest_exists = event.path in dest.files
            dpath = os.path.join(dest.path, event.path)

            # need to copy file from source to dest
            if source_exists and not dest_exists:
                self.copyfile(spath, dpath)

            # need to remove file from dest
            elif dest_exists and not source_exists:
                if os.path.exists(dpath):
                    self.safe_delete(dpath)

                del dest.files[event.path]

            # don't need to do anything, do we?
            elif not source_exists and not dest_exists:
                pass

            # file exists in both places, so it's an update
            else:
                self.copyfile(spath, dpath)

            # elif action.name == 'rename':
            #     before = os.path.join(self.args.destination, action.old_path)
            #     after = os.path.join(self.args.destination, action.path)
            #     print(self.count, '--> rename', before, 'to', after)
            #     os.rename(before, after)


    def main(self):
        self.setup()

        for src in self.sources:
            for dest in self.destinations[src.project.name]:
                print(src, dest)
                self.presync(src, dest)

        log('watching for changes')

        try:
            for event in self.get_events():
                self.process(event)

        except KeyboardInterrupt:
            log('terminated')

        finally:
            # cache target state to improve startup time
            for t in self.targets:
                t.save_state()



# graft the older standalone code into the tart utility
class Command(command.Command):
    def run(self, args):
        app = QuickDeploy(args)
        app.main()


# EOF
