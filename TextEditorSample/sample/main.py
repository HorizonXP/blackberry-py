import os
import sys

from bbpy.app import Application

from .editor import Editor

APPDIR = os.path.dirname(__file__)

class App(Application):
    def __init__(self):
        super(App, self).__init__()

        self.editor = Editor(self)


    def run(self):
        v = self.create_view()

        # add local dir to imports for development
        v.engine().addImportPath(APPDIR)

        rc = v.engine().rootContext()
        rc.setContextProperty('editor', self.editor)

        v.setSource(os.path.join(APPDIR, 'main.qml'))
        v.showFullScreen()

        super(App, self).run()


def main():
    app = App()
    app.run()
