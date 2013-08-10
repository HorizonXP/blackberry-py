import os
import ctypes as ct
import json

import tart

from . import navigator_invoke as ni


class App(tart.Application):
    def __init__(self):
        super().__init__(debug=False)   # set True for some extra debug output

        with open('sharewith/pim/testfile.txt', 'w') as f:
            f.write('Wheeee! This is my content.\n')

        # install BPS event handler for navigator events
        from . import navigator_handler
        navigator_handler.NavigatorHandler(self.bps_dispatcher)


    def onUiReady(self):
        # These need to be absolute paths for the C++ approach (app.composeEmail)
        # but for some reason not when we're directly invoking via Python.
        self.paths = [
            # os.path.abspath('shared/misc/testfile.txt'),
            # os.path.abspath('/accounts/1000/shared/camera/IMG_00000043.png'),
            os.path.abspath('sharewith/pim/testfile.txt'),
            ]

        tart.send('filePathUpdated', paths=self.paths)


    def onGetHelp(self):
        helppath = os.path.join(os.path.dirname(__file__), '../assets/help.html')
        with open(helppath, encoding='utf-8') as f:
            tart.send('gotHelp', text=f.read().strip().replace('\n', ' '))


    invoke_id = 17

    def onTestInvoke(self, data):
        print('onTestInvoke', data)

        invoke = self.invoke = ct.POINTER(ni.navigator_invoke_invocation_t)()
        ni.navigator_invoke_invocation_create(ct.byref(invoke))

        # set invocation properties
        ni.navigator_invoke_invocation_set_action(invoke, b'bb.action.COMPOSE')
        ni.navigator_invoke_invocation_set_type(invoke, b'message/rfc822')

        # the id is not the same as actionId, and is retrieved with navigator_event_get_id()
        self.invoke_id += 1
        ni.navigator_invoke_invocation_set_id(invoke, str(self.invoke_id).encode('ascii'))

        data = b'data:json:' + data.encode('utf8') + b'\n'
        ni.navigator_invoke_invocation_set_data(invoke, data, len(data))

        # invoke the target
        ni.navigator_invoke_invocation_send(invoke)

        # check id
        invoke_id = ni.navigator_invoke_invocation_get_id(invoke)
        print('sent invoke id', invoke_id)

        # clean up resources
        ni.navigator_invoke_invocation_destroy(invoke)


# EOF
