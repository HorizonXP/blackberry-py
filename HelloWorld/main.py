import os
import sys

ENVDIR = os.path.dirname(__file__)
sys.path.append(os.path.join(ENVDIR, 'blackberry-py'))

from PySide.QtCore import QUrl
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView

app = QApplication(sys.argv)

# set up the QML part of things
view = QDeclarativeView()
qmlpath = os.path.join(ENVDIR, 'main.qml')
view.setSource(QUrl.fromLocalFile(qmlpath))
view.show()

# Enter Qt application main loop
sys.exit(app.exec_())
