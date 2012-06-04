import sys

from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView

app = QApplication(sys.argv)

view = QDeclarativeView()
view.setSource('app/python/main.qml')
view.show()

app.exec_()
