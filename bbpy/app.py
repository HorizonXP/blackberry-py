'''BlackBerry-Py base application class.'''

import sys

from PySide.QtCore import qDebug, QObject, Signal, Slot, Qt
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView

from .loader import Loader

from .bpsloop import BpsThread
bpsThread = BpsThread()
bpsThread.start()


class BBPyView(QDeclarativeView):
    # signals
    swipeDown = Signal()    # user performed swipe down from top bezel

    def keyPressEvent(self, e):
        # qDebug(':view]-keyPress {}{}'.format(e.type(), ' spont.' if e.spontaneous() else ''))
        if e.key() == Qt.Key_Menu:
            self.swipeDown.emit()
            # qDebug('emitted swipeDown ')
        return super(BBPyView, self).keyPressEvent(e)



class Application(QApplication):
    # signals

    # user performed swipe down from top bezel
    swipeDown = Signal()

    # keyboard show/hide and availableGeometry (size) change
    keyboardChange = Signal(bool, 'QVariant')

    # notification from our own bps event handler
    bpsEvent = Signal(str)


    def onBpsEvent(self, msg):
        qDebug('BPS: ' + msg)


    def __init__(self, qml=None):
        super(Application, self).__init__(sys.argv)

        self._view = None

        # configure to process resizes and update keyboard visibility/height
        d = self._desktop = self.desktop()
        d.workAreaResized.connect(self.desktopResized)
        self._initial_size = d.size().toTuple()

        if qml:
            v = self.create_view()
            v.setSource(qml)
            v.showFullScreen()


    dataLoaded = Signal(str, str)

    @Slot(str, str)
    def onDataLoaded(self, url, filename):
        '''Loader thread has retrieved remote image and stored as temp file'''
        # print('stored', url, 'as', filename)
        root = self._view.rootObject()
        images = root.findChildren(QObject, url)
        for img in images:
            img.setProperty('source', filename)


    @Slot(str)
    def loadImageSource(self, url):
        '''for requests from FixedImage to load remote image data'''
        # print('load', url)
        if not hasattr(self, 'loader'):
            self.dataLoaded.connect(self.onDataLoaded, Qt.QueuedConnection)
            self.loader = Loader(self.dataLoaded)
            self.loader.start()
        self.loader.load_url(url)


    @Slot(int)
    def desktopResized(self, index):
        size = self._desktop.availableGeometry(index).size()
        # qDebug('screen {} resized: {}'.format(index, size))
        w, h = size.toTuple()
        visible = h not in self._initial_size

        # Counter-hack to go with the "huge hack" for Qt blackberry
        # plugin when it's using the PPS keyboard stuff instead of BPS.
        # Should be removed as soon as we move to a Qt build that
        # uses the BPS approach.
        if visible:
            size.setHeight(h - 8)

        self.keyboardChange.emit(visible, size)
        # qDebug('keyboardChange({}, {})'.format(visible, size))


    def create_view(self):
        # view, root, and scene all seem to get a WindowActivate/Deactivate event
        # when app goes inactive etc; view also gets an ActivationChange event
        # and FocusIn/Out events
        self._view = v = BBPyView()
        v.setResizeMode(v.ResizeMode.SizeRootObjectToView)
        rc = v.rootContext()
        rc.setContextProperty('bbpy', self)
        return v


    def run(self):
        if sys.platform == 'qnx6':
            if self._view:
                self._view.swipeDown.connect(self.swipeDown)

        bpsThread.signal = self.bpsEvent
        self.bpsEvent.connect(self.onBpsEvent, Qt.QueuedConnection)
        qDebug('window group is {}'.format(bpsThread.windowGroup))

        # Enter Qt application main loop
        sys.exit(self.exec_())


# EOF
