import os
import sys
import time

from ctypes import *

qtcore = CDLL('libQtCore.so.4')
qtcascades = CDLL('libQtCascades.so')
qtdecl = CDLL('libQtDeclarative.so.4')

qDebug = qtcore._Z6qDebugPKcz
qMalloc = qtcore._Z7qMallocj
QString_QChar_p = qtcore._ZN7QStringC1EPK5QChar
QUrl_constructor = qtcore._ZN4QUrlC1ERK7QString
QThread_initialize = qtcore._ZN7QThread10initializeEv
QCoreApplication_startingUp = qtcore._ZN16QCoreApplication10startingUpEv
QCoreApplication_exec = qtcore._ZN16QCoreApplication4execEv

Application_constructor = qtcascades._ZN2bb8cascades11ApplicationC1ERiPPc
Application_setScene = qtcascades._ZN2bb8cascades11Application8setSceneEPNS0_12AbstractPaneE
QmlDocument_constructor = qtcascades._ZN2bb8cascades11QmlDocumentC1Ev
QmlDocument_load = qtcascades._ZN2bb8cascades11QmlDocument4loadERK7QString
QmlDocument_hasErrors = qtcascades._ZN2bb8cascades11QmlDocument9hasErrorsEv
QmlDocument_createRootNode = qtcascades._ZN2bb8cascades11QmlDocument14createRootNodeINS0_8UIObjectEEEPT_P19QDeclarativeContext

def bLog(msg):
    qDebug(msg.encode('ascii'))


class App(object):
    def run(self):
        try:
            argc = c_long(1)
            argv_0 = sys.argv[0].encode('ascii')
            argv_0_p = c_char_p(argv_0)
            argv = pointer(argv_0_p)

            # QThread_initialize()

            # sizeof(Qapplication) == 8
            app = qMalloc(8)
            Application_constructor(app, byref(argc), argv)

            bLog('starting up: {}'.format(QCoreApplication_startingUp()))

            # The QmlDocument.load() routine seems to insist on the file
            # being stored in app/native/assets, which we don't have, so
            # we have to use a relative path to get up out of there.
            # It ignores attempts at making absolute paths.
            p = '../../python/lite/main.qml'

            # Python is using 32-bit chars on QNX (UTF32) whereas
            # Qt things QChars are 16-bit, so we need some hackery
            # to convert, with special attention to the NUL terminator
            # since that also has to be 16-bits
            buf = create_string_buffer((p + '\0').encode('utf-16-le'))

            # sizeof(QString) == 8
            qs1 = qMalloc(8)
            QString_QChar_p(qs1, buf)

            qml = qMalloc(32)
            QmlDocument_constructor(qml)

            rc = QmlDocument_load(qml, qs1)
            bLog('load rc = {}'.format(rc))

            if not QmlDocument_hasErrors(qml):
                page = QmlDocument_createRootNode(qml, None)
                bLog('page = {}'.format(page))
                if page:
                    Application_setScene(page)

            rc = QCoreApplication_exec(app)
            bLog('rc = {}'.format(rc))

        finally:
            bLog('app.run() done!')



def main():
    global app # make it global so CLI can find it
    app = App()
    app.run()

