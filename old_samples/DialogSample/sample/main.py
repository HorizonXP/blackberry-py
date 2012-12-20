import os
import sys

from bbpy.app import Application

from PySide.QtCore import (Qt, QObject, Signal, Slot, Property, qDebug)

from qnx.dialog import Dialog, make_button


class App(Application):

    def __init__(self):
        super(App, self).__init__()
        self.dlg = None


    def get_dialog_id(self):
        self.dlg_id = getattr(self, 'dlg_id', 0) + 1
        return self.dlg_id


    @Slot('QVariant')
    def do_dialog(self, params):
        qDebug('do_dialog {}'.format(params))

        # :param position: one of "topCenter", "middleCenter", or "bottomCenter"
        #     (default is "middleCenter")
        # :param size: The size of the dialog box. One of "small", "medium",
        #     "large", "tall" or "full" (default is "medium")

        settings = {}
        settings['dtype'] = getattr(Dialog, 'TYPE_{}'.format(params.get('type', 'alert').upper()))

        settings['bkgAlpha'] = 0.5
        try:
            settings['buttons'] = params['buttons']
        except KeyError:
            pass

        if not params.get('modal'):
            # dialogs need to have this in order not to be system-modal
            from bbpy.app import bpsThread
            qDebug('sweet! windowGroup is {}'.format(bpsThread.windowGroup))
            settings['groupId'] = bpsThread.windowGroup

        settings['position'] = params.get('position', 'middleCenter')
        settings['size'] = params.get('size', 'medium')
        try:
            settings['filter'] = params['filter']
        except KeyError:
            pass

        settings['titleText'] = params.get('title', 'No Title')
        # :param titleHtmlText: title string to display in html (this attribute
        #     trumps ``titleText``)

        try:
            settings['messageText'] = params['messageText']
        except KeyError:
            pass

        # files = ['testing', 'this']
        # buttonOkay = make_button('OK')
        # buttonCancel = make_button('Cancel')
        # dialogPicker = Dialog(42, Dialog.TYPE_POPUP,
        #     buttons=[buttonCancel, buttonOkay], groupId=groupId, items=files, bkgAlpha=0.25)
        # dialogPicker.show_for_response(titleText='Select a script',
        #     messageText='Enter a file to run')

        # qDebug('showed the dialog {}'.format(dialogPicker))

        self.make_dialog(settings)
        self.show_dialog()


    def make_dialog(self, settings):
        if self.dlg:
            self.cancel_dialog()

        dtype = settings.pop('dtype')
        qDebug('dialog of type {}'.format(dtype))
        if 'buttons' not in settings:
            settings['buttons'] = [{Dialog.BUTTON_LABEL: Dialog.LABEL_OK}]
        self.dlg = Dialog(self.get_dialog_id(), dtype, **settings)


    def show_dialog(self):
        self.dlg.show_for_response()


    def cancel_dialog(self):
        self.dlg.cancel()
        self.dlg = None


    @Slot()
    def onLoaded(self):
        pass


    def run(self):
        v = self.create_view()
        v.statusChanged.connect(self.onLoaded)

        rc = v.engine().rootContext()
        rc.setContextProperty('engine', self)

        p = os.path.join(os.path.dirname(__file__), 'main.qml')
        v.setSource(p)
        v.showFullScreen()

        self.root = v.rootObject()

        super(App, self).run()



def main():
    global app # make it global so CLI can find it
    app = App()
    app.run()
