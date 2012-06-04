import os
import sys

from bbpy.app import Application

from PySide.QtGui import QGraphicsView
from PySide.QtOpenGL import QGLFormat, QGLWidget

from .Twitter import Twitter


class App(Application):
    def __init__(self):
        super(App, self).__init__()

        self.setGraphicsSystem('opengl')


    def run(self):
        twitter = Twitter()
        twitter.consumerKey = 'XIeqUJ941sRdsuPfbnvcFg'
        twitter.consumerSecret = '3WibMeldSeLN1BfSpjmUzHd5FGWjlRgwsQqZwcKitA'

        format = QGLFormat.defaultFormat()
        format.setSampleBuffers(False)
        format.setSwapInterval(1)
        glWidget = QGLWidget(format)
        glWidget.setAutoFillBackground(False)

        v = self.create_view()
        rc = v.engine().rootContext()
        rc.setContextProperty("twitter", twitter)

        v.setViewport(glWidget)
        v.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        v.setSource(os.path.join(os.path.dirname(__file__), 'main.qml'))
        v.show()

        self.root = v.rootObject()

        super(App, self).run()


def main():
    try:
        global app
        app = App()
        app.run()
    finally:
        sys.stdout.flush()
        sys.stderr.flush()

if __name__ == '__main__':
    main()
