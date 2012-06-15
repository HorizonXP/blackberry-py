import os
import sys
import threading
import datetime as dt

from bbpy import Application

from PySide.QtCore import QObject, Slot, Signal, qDebug
from PySide.QtGui import QFont


class App(Application):
    def run(self):
        # view, root, and scene all seem to get a WindowActivate/Deactivate event
        # when app goes inactive etc; view also gets an ActivationChange event
        # and FocusIn/Out events
        v = self.create_view()
        qmlpath = os.path.join(os.path.dirname(__file__), 'main.qml')
        v.setSource(qmlpath)

        v.showFullScreen()

        # Enter Qt application main loop
        super(App, self).run()


def main():
    # store global reference so we can find it via telnet CLI
    global app
    app = App()
    app.run()


if __name__ == '__main__':
    main()
