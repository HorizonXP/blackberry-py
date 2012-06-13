import os
import sys
import time

from ctypes import *

BBPYPATH = 'shared/misc/blackberry-py'
# BBPYPATH = 'app/python/blackberry-py'

if sys.platform == 'qnx6':
    os.environ['LD_LIBRARY_PATH'] = os.path.join(BBPYPATH, 'lib')
    os.environ['QT_PLUGIN_PATH'] = os.path.join(BBPYPATH, 'plugins')
    os.environ['QML_IMPORT_PATH'] = os.path.join(BBPYPATH, 'imports')
    os.environ['QT_QPA_PLATFORM'] = 'blackberry'

# from pprint import pprint
# pprint(dict(os.environ), stream=sys.stderr)
# pprint(sys.path, stream=sys.stderr)
# pprint(os.getcwd(), stream=sys.stderr)
# pprint(sys.argv, stream=sys.stderr)
# sys.stderr.flush()

qtcore = CDLL('libQtCore.so.4')
qtgui = CDLL('libQtGui.so.4')
qtdecl = CDLL('libQtDeclarative.so.4')
bb = CDLL(os.path.join(os.environ['QT_PLUGIN_PATH'], 'platforms/libblackberry.so'))

qDebug = qtcore._Z6qDebugPKcz
qMalloc = qtcore._Z7qMallocj
QString_QChar_p = qtcore._ZN7QStringC1EPK5QChar
QUrl_constructor = qtcore._ZN4QUrlC1ERK7QString
QThread_initialize = qtcore._ZN7QThread10initializeEv
QCoreApplication_startingUp = qtcore._ZN16QCoreApplication10startingUpEv

QApplication_constructor = qtgui._ZN12QApplicationC1ERiPPc
QApplication_exec = qtgui._ZN12QApplication4execEv
QWidget_setVisible = qtgui._ZN7QWidget10setVisibleEb
QApplication_type = qtgui._ZN12QApplication4typeEv
QWidget_showFullScreen = qtgui._ZN7QWidget14showFullScreenEv

QDeclarativeView_constructor = qtdecl._ZN16QDeclarativeViewC1EP7QWidget
QDeclarativeView_setSource = qtdecl._ZN16QDeclarativeView9setSourceERK4QUrl
QDeclarativeView_setResizeMode = qtdecl._ZN16QDeclarativeView13setResizeModeENS_10ResizeModeE

ResizeMode_SizeViewToRootObject = 0
ResizeMode_SizeRootObjectToView = 1

def bLog(msg):
    qDebug(msg.encode('ascii'))


class App(object):
    def run(self):
        try:
            argc = c_long(1)
            argv_0 = sys.argv[0].encode('ascii')
            argv_0_p = c_char_p(argv_0)
            argv = pointer(argv_0_p)

            bLog('gui used? {0.value}'.format(c_long.in_dll(qtgui, 'qt_is_gui_used')))

            # QThread_initialize()

            # sizeof(Qapplication) == 8
            app = qMalloc(8)
            QApplication_constructor(app, byref(argc), argv)

            bLog('starting up: {}'.format(QCoreApplication_startingUp()))
            bLog('gui used? {0.value}'.format(c_long.in_dll(qtgui, 'qt_is_gui_used')))
            bLog('qt_appType {}'.format(QApplication_type()))

            p = os.path.join(os.path.dirname(__file__), 'main.qml')

            # Python is using 32-bit chars on QNX (UTF32) whereas
            # Qt things QChars are 16-bit, so we need some hackery
            # to convert, with special attention to the NUL terminator
            # since that also has to be 16-bits
            buf = create_string_buffer((p + '\0').encode('utf-16-le'))

            # sizeof(QString) == 8
            qs1 = qMalloc(8)
            QString_QChar_p(qs1, buf)

            # sizeof(QUrl) == 8
            qurl = qMalloc(8)
            QUrl_constructor(qurl, qs1)

            # sizeof(QDeclarativeView) == 20
            view = qMalloc(20)
            QDeclarativeView_constructor(view, None)

            QDeclarativeView_setSource(view, qurl)

            # Note: the default of SizeViewToRootObject, or using just show()
            # or setVisible(1) instead of showFullScreen(), results in the QML
            # root element not having a size, or being resized properly when
            # you rotate the device
            QDeclarativeView_setResizeMode(view, ResizeMode_SizeRootObjectToView)
            QWidget_showFullScreen(view)

            QApplication_exec(app)

        finally:
            bLog('app.run() done!')


def main():
    global app # make it global so CLI can find it
    app = App()
    app.run()


# launch telnet-based command line interface (CLI)
# if '--cli' in sys.argv:
#     try:
#         import cli
#     except ImportError:
#         print('unable to import cli, ignoring --cli option', file=sys.stderr)
#     else:
#         import threading
#         t = threading.Thread(target=cli.run)
#         t.daemon = True
#         t.start()
