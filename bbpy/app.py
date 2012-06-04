'''BlackBerry-Py base application class.'''

import os
import sys

from PySide.QtCore import Slot
from PySide.QtGui import QApplication


class Application(QApplication):
    def __init__(self, qml=None):
        super(Application, self).__init__(sys.argv)

        # path to QML file, if we should use QDeclarativeView
        self._qml = qml


    @Slot()
    def _onDesktopResized(self, *args):
        '''this occurs when we rotate after starting up'''
        w, h = self.desktop().size().toTuple()
        self._view.setFixedSize(w, h)
        # after this we get a spurious(?) onSceneRectChanged
        # but the desktop size is still correct...


    @Slot()
    def _onSceneRectChanged(self, *args):
        '''we get this on initial startup, though the rect is (0,0,1020,157)
        but then we also get a duplicate with 1024,600 a moment later'''
        w, h = self.desktop().size().toTuple()
        # this triggers the root to resize if using SizeRootObjectToView
        # this triggers the root onWidth/HeightChanged routines
        # this triggers onSceneResized()
        self._view.setFixedSize(w, h)


    def run(self):
        if self._qml:
            desktop = self.desktop()
            desktop.resized.connect(self._onDesktopResized)

            # view, root, and scene all seem to get a WindowActivate/Deactivate event
            # when app goes inactive etc; view also gets an ActivationChange event
            # and FocusIn/Out events
            from PySide.QtDeclarative import QDeclarativeView

            self._view = v = QDeclarativeView()
            v.setResizeMode(v.ResizeMode.SizeRootObjectToView)
            v.setSource(self._qml)
            v.show()

            scene = v.rootObject().scene()
            scene.sceneRectChanged.connect(self._onSceneRectChanged)

        # Enter Qt application main loop
        sys.exit(self.exec_())

