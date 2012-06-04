import os
import sys

APPDIR = os.path.dirname(__file__)
sys.path.append(os.path.join(APPDIR, 'blackberry-py'))

from PySide.QtCore import QUrl
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView


def main():
    app = QApplication(sys.argv)

    # set up the QML part of things
    view = QDeclarativeView()
    qmlpath = os.path.join(APPDIR, 'main.qml')
    view.setSource(QUrl.fromLocalFile(qmlpath))
    view.show()

    # Enter Qt application main loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
