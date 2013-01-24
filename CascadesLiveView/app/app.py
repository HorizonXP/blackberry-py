import os
import sys
import threading
import time
import shutil
import queue
import glob
import re

import tart


class FileMonitor(threading.Thread):
    CHECK_PERIOD = 1.0  # seconds between checks for changes

    CLONE_FMT = '_liveview-{}.qml'
    CLONE_PAT = r'_liveview-\d+.qml'

    def __init__(self, target):
        super().__init__()
        self.daemon = True

        print('will monitor', target)
        self.target = target
        self.folder = os.path.dirname(self.target)
        print('in folder', self.folder)
        self.counter = 0
        self.prev_clone = None
        self._prev_sigs = {}

        self.queue = queue.Queue()


    def terminate(self):
        self.queue.put(None)


    def run(self):
        while True:
            # wait for some time or for someone to signal us
            try:
                msg = self.queue.get(timeout=self.CHECK_PERIOD)
            except queue.Empty:
                pass
            else:
                print('got', msg)
                if msg is None:
                    break
                # process msg, if any

            changed = []
            for target in os.listdir(self.folder):
                if not target.endswith('.qml'):
                    # print('ignoring', target)
                    continue
                if re.match(self.CLONE_PAT, target):
                    # print('ignoring', target)
                    continue

                tpath = os.path.join(self.folder, target)
                stat = os.stat(tpath)
                signature = (stat.st_mtime, stat.st_size)
                if signature != self._prev_sigs.get(target):
                    print('sig', target, signature)
                    self._prev_sigs[target] = signature
                    changed.append(target)

            if changed:
                print('files changed: {}'.format(', '.join(sorted(changed))))
                path = self.clone_target()
                tart.send('fileChanged', path=path)


    def clone_target(self):
        base, ext = os.path.splitext(self.target)
        self.counter += 1

        clone = os.path.join(self.folder, self.CLONE_FMT.format(self.counter))
        print('copy', self.target, 'to', clone)
        shutil.copy(self.target, clone)

        if self.prev_clone and os.path.exists(self.prev_clone):
            try:
                os.remove(self.prev_clone)
                print('removed old', self.prev_clone)
            except OSError as ex:
                print('error removing', self.prev_clone, ex)
                pass
        self.prev_clone = clone

        return clone



class App(tart.Application):
    def __init__(self):
        super().__init__(debug=False)   # set True for some extra debug output
        self.monitor = None
        self.path = None


    def onUiReady(self):
        pass


    def onManualExit(self):
        self.cleanup()
        tart.send('continueExit')


    def cleanup(self):
        if self.path:
            pat = os.path.join(os.path.dirname(self.path), '_liveview-*.qml')
            for path in glob.glob(pat):
                try:
                    os.remove(path)
                    print('removed', path)
                except OSError as ex:
                    print('error removing', path, ex)
                    pass


    def onMonitorFile(self, path):
        self.path = path

        if self.monitor:
            print('kill old monitor')
            self.monitor.terminate()
            self.cleanup()

        self.monitor = FileMonitor(path)
        self.monitor.start()


# EOF
