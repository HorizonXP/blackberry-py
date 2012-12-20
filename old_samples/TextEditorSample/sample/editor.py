
import os
import shutil

from PySide.QtCore import QObject, qDebug, Property, Signal, Slot


class Editor(QObject):

    fileListChanged = Signal(str, 'QVariant')

    fileLoaded = Signal(str, str)


    def __init__(self, app):
        super(Editor, self).__init__()

        self.app = app

        self._fileText = ''
        self._folder = '/accounts/1000/shared/misc'
        self._filepath = ''


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
                    yield item
                else:
                    yield '?' + item + '?'

        items = list(filter_list(self._folder))
        qDebug('filelist {}'.format(items))
        if self._folder != '/':
            items.insert(0, '../')
        self.fileListChanged.emit(self._folder, sorted(items))


    @Slot(str)
    def do_select(self, name):
        if name == '.. (parent folder)':
            name = '..'
        path = os.path.normpath(os.path.join(self._folder, name))
        qDebug('select ' + path)
        if os.path.isfile(path):
            qDebug('open file ' + path)
            self.filepath = path
            self.fileText = open(path, encoding='utf-8').read()
            self.fileLoaded.emit(self.filepath, self.fileText)
        else:
            qDebug('is dir')
            self.folder = path
            self.do_get_filelist()


    # the decorator is required for QML to see this
    @Slot()
    def do_new(self):
        qDebug('new')
        self.filepath = ''
        self.fileText = ''
        self.fileTextChanged.emit()
        self.fileLoaded.emit(self.filepath, self.fileText)


    @Slot()
    def do_load(self):
        qDebug('load')


    @Slot(str)
    def do_save(self, text):
        qDebug('saving {} chars'.format(len(text)))

        # make a backup
        backup = self.filepath + '~'
        shutil.copyfile(self.filepath, backup)
        qDebug('backed up to {}'.format(backup))

        with open(self.filepath, 'w', encoding='utf-8') as savefile:
            savefile.write(text)
        qDebug('saved')


    @Slot(str)
    def do_dialog(self, dtype):
        qDebug('dialog ' + dtype)


    @Slot()
    def open(self, name):
        qDebug('open ' + name)
        self.fileTextChanged.emit()


    @Signal
    def fileTextChanged(self): pass

    def _getFileText(self):
        return self._fileText

    def _setFileText(self, newval):
        self._fileText  = newval

    fileText = Property(str, _getFileText, _setFileText, notify=fileTextChanged)


    def _getFolder(self):
        return self._folder

    def _setFolder(self, newval):
        self._folder  = newval

    folder = Property(str, _getFolder, _setFolder)


    # Property: filepath
    filepathChanged = Signal()
    def _get_filepath(self):
        return self._filepath
    def _set_filepath(self, value):
        self._filepath = value
        self.filepathChanged.emit()
    filepath = Property(str, _get_filepath, _set_filepath, notify=filepathChanged)


# EOF
