
from bb import bps
import tart

from .navigator_invoke import *


class NavigatorHandler:
    def __init__(self, dispatcher):
        rc = bps.navigator_request_events(0)
        if rc == bps.BPS_FAILURE:
            raise Exception('locale request events failed')

        dispatcher.add_handler(bps.navigator_get_domain(), self.handle_event)


    #---------------------------------------------
    #
    def handle_event(self, event):
        '''Handle BPS events for our domain'''
        code = bps.bps_event_get_code(event)

        # print('NAV: {}, 0x{:x}'.format(code, code))

        if code == bps.NAVIGATOR_INVOKE_TARGET:
            print('NAVIGATOR_INVOKE_TARGET')

            invoke = navigator_invoke_event_get_invocation(event)
            print('invoke is', invoke)

            invoke_id = navigator_invoke_invocation_get_id(invoke)
            print('invoke id', invoke_id)

            target = navigator_invoke_invocation_get_target(invoke)
            print('target', target)

            action = navigator_invoke_invocation_get_action(invoke)
            print('action', action)

        elif code == bps.NAVIGATOR_INVOKE_TARGET_RESULT:
            print('NAVIGATOR_INVOKE_TARGET_RESULT')

            # this retrieves the id set with navigator_invoke_invocation_set_id()
            print('nav id', bps.navigator_event_get_id(event))

            print('nav err', bps.navigator_event_get_err(event))


            # print('target', navigator_invoke_event_get_target(event))
            # print('target type', navigator_invoke_event_get_target_type(event))
            # print('group id', navigator_invoke_event_get_group_id(event))
            # print('dname', navigator_invoke_event_get_dname(event))



# EOF
