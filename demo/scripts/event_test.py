'''Demonstrate/test event handling.'''

import sys
import time
#~ import qnx.notification as qn
from bbxpy.wrapped.bps import virtualkeyboard_request_events


def run():
    import bbxrun
    screen = bbxrun.screen

    virtualkeyboard_request_events(0)

    start = time.time()
    while time.time() - start < 6:
        screen.poll()
        time.sleep(0.05)
