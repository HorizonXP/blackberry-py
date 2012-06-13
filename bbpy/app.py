'''BlackBerry-Py base application class.'''

import sys

from PySide.QtCore import qDebug, Signal, Qt
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView


class BBPyView(QDeclarativeView):
    # signals
    swipeDown = Signal()    # user performed swipe down from top bezel

    def keyPressEvent(self, e):
        # qDebug(':view]-keyPress {}{}'.format(e.type(), ' spont.' if e.spontaneous() else ''))
        if e.key() == Qt.Key_Menu:
            self.swipeDown.emit()
            qDebug('emitted swipeDown ')
        return super(BBPyView, self).keyPressEvent(e)



class Application(QApplication):
    # signals
    swipeDown = Signal()    # user performed swipe down from top bezel


    def event(self, e):
        # qDebug(':app]-event {}{}'.format(e.type(), ' spont.' if e.spontaneous() else ''))
        return super(Application, self).event(e)


    def __init__(self, qml=None):
        super(Application, self).__init__(sys.argv)

        self._view = None

        if qml:
            v = self.create_view()
            v.setSource(qml)
            v.showFullScreen()


    def create_view(self):
        # view, root, and scene all seem to get a WindowActivate/Deactivate event
        # when app goes inactive etc; view also gets an ActivationChange event
        # and FocusIn/Out events
        self._view = v = BBPyView()
        v.setResizeMode(v.ResizeMode.SizeRootObjectToView)
        return v


    def run(self):
        if sys.platform == 'qnx6':
            if self._view:
                self._view.swipeDown.connect(self.swipeDown)

        # Enter Qt application main loop
        sys.exit(self.exec_())

