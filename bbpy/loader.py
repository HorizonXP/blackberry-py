'''Loader thread to assist with loading remote Images for broken Qt port.'''

import os
import threading
import urllib.request
import tempfile
import queue


class Loader(threading.Thread):
    def __init__(self, signal):
        super(Loader, self).__init__()
        self.signal = signal
        self.queue = queue.Queue()
        self.daemon = True


    def load_url(self, url):
        self.queue.put(url)


    def run(self):
        while True:
            url = self.queue.get()
            # print('requesting', url)

            f = urllib.request.urlopen(url)
            data = f.read()
            # print('read {} bytes'.format(len(data)))

            # make temp file use the correct suffix in case it matters...
            # TODO: check whether it matters
            _, ext = os.path.splitext(url)
            t = tempfile.NamedTemporaryFile(mode='wb', suffix=ext, delete=False)
            t.write(data)
            t.close()

            self.signal.emit(url, t.name)
            # print('signalled, file', t.name)

