import os
import sys
import threading
import time
import shutil
import re

from bbpy.app import Application

from PySide.QtCore import (Qt, QObject, Signal, Slot, Property, qDebug)

APPDIR = os.path.dirname(__file__)
TEMPFILE_PATTERN = re.compile(r'_qv_\d+.qml')


class FileMonitor(threading.Thread):
    CHECK_PERIOD = 1.0  # seconds between checks for changes

    def __init__(self, signal):
        super(FileMonitor, self).__init__()
        self.daemon = True

        self.signal = signal

        self._target = None
        self._prev_signature = None

        self.event = threading.Event()


    def _getTarget(self):
        return self._target

    def _setTarget(self, path):
        self._target = path
        self.event.set()

    target = property(_getTarget, _setTarget)


    def run(self):
        while True:
            # wait for some time or for someone to signal us
            self.event.wait(timeout=self.CHECK_PERIOD)
            self.event.clear()

            if self._target is not None:
                stat = os.stat(self._target)
                signature = (self._target, stat.st_mtime, stat.st_size)
                if signature != self._prev_signature:
                    self._prev_signature = signature
                    qDebug('file changed: {}'.format(self._target))
                    self.signal.emit(self._target)



class App(Application):
    # signals
    fileListChanged = Signal(list)
    fileLoaded = Signal(str)
    fileChanged = Signal(str)  # file contents changed on-disk


    def __init__(self):
        super(App, self).__init__()

        self._tempPath = None
        self._rootId = None
        self._errors = ''

        self._folder = '.'
        self.filelist = []


    def loadQml(self, path, id):
        self._rootId = id
        # if path[1] == ':':
        #     path = path[2:].replace('\\', '/')
        qDebug('setSource {}: {}'.format(id, path))
        self._view.setSource(path)


    def loadTempQml(self, path):
        # hack to avoid problems with QML triggering a setSource() etc
        if self._tempPath:
            os.remove(self._tempPath)

        # TODO: use QDeclarativeEngine.clearComponentCache() to
        # remove need to use temporary files?
        folder = os.path.dirname(path)
        self._tempPath = os.path.join(folder,
            '_qv_{}.qml'.format(hash(os.stat(path).st_mtime)))
        shutil.copyfile(path, self._tempPath)

        self.loadQml(self._tempPath, id='test_page')


    @Slot()
    def onLoaded(self):
        qDebug('loading {}, state: {}'.format(self._rootId,
            str(self._view.status()).rsplit('.', 1)[-1]))
        qDebug('source: {}'.format(self._view.source()))
        root = self._view.rootObject()
        qDebug('root: ' + str(root))
        qDebug('view.children: ' + str(self._view.children()))
        if self._rootId == 'error_page':
            root.returnHome.connect(self.showMainPage, Qt.QueuedConnection)

        elif self._rootId == 'main_page':
            self.fileListChanged.connect(root.onFileListChanged, Qt.QueuedConnection)
            self.fileLoaded.connect(root.onFileLoaded, Qt.QueuedConnection)
            self.do_get_filelist()

        elif self._rootId == 'test_page':
            errors = self._view.errors()
            if errors:
                self._errors = '\n'.join(str(x) for x in errors)
                errpage = os.path.join(APPDIR, 'error_page.qml')
                # errpage = errpage.replace('\\', '/')[2:]
                self.loadQml(errpage, id='error_page')


    @Slot()
    def showMainPage(self):
        p = os.path.join(os.path.dirname(__file__), 'main.qml')
        self.loadQml(p, id='main_page')


    @Slot()
    def do_get_filelist(self):
        qDebug('list for ' + self._folder)
        items = []
        def filter_list(folder):
            for item in os.listdir(folder):
                path = os.path.join(folder, item)
                if os.path.isdir(path):
                    yield item + '/'
                elif os.path.isfile(path):
                    if path.endswith('.qml'):
                        yield item

        items = list(filter_list(self._folder))
        if self._folder != '/':
            items.insert(0, '.. (parent folder)')
        self.fileListChanged.emit(items)


    @Slot(str)
    def do_select(self, name):
        qDebug('-' * 40)
        qDebug('do_select ' + name)
        if name == '.. (parent folder)':
            name = '..'
        path = os.path.normpath(os.path.join(self._folder, name))
        qDebug('select ' + path)
        if os.path.isfile(path):
            self.filemon.target = path
        else:
            qDebug('is dir')
            self.remove_tempfiles(path)
            self._folder = path
            self.do_get_filelist()


    def remove_tempfiles(self, path):
        '''Clean out any leftover temporary files we created.'''
        qDebug('remove temp files')
        for name in os.listdir(path):
            qDebug('check ' + name)
            if TEMPFILE_PATTERN.match(name):
                target = os.path.join(path, name)
                qDebug('removing ' + target)
                os.remove(target)


    def _getErrors(self):
        return self._errors
    errorsChanged = Signal()
    errors = Property(str, _getErrors, notify=errorsChanged)


    def run(self):
        v = self.create_view()
        v.statusChanged.connect(self.onLoaded, Qt.QueuedConnection)

        rc = v.engine().rootContext()
        rc.setContextProperty('engine', self)

        p = os.path.join(os.path.dirname(__file__), 'main.qml')
        self.loadQml(p, id='main_page')
        v.show()

        self.root = v.rootObject()

        self.fileChanged.connect(self.loadTempQml, Qt.QueuedConnection)
        self.filemon = FileMonitor(signal=self.fileChanged)
        self.filemon.start()

        super(App, self).run()


def main():
    global app # make it global so CLI can find it
    app = App()
    app.run()
