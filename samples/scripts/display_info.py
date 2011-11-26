'''Report information about the attached displays.'''

import sys
import os
import time
import random
from ctypes import byref, cast, sizeof, c_int, c_void_p, pointer, create_string_buffer

from bbxpy.wrapped.screen import *
from bbxpy.wrapped.img import *

def showptr(p):
    return p.contents if p else 'NULL'


def run():
    import bbxrun
    screen = bbxrun.screen

    time.sleep(1)

    intval = c_int()
    rc = screen_get_context_property_iv(screen.screen_ctx, SCREEN_PROPERTY_DISPLAY_COUNT, byref(intval))
    if rc: raise RuntimeError(rc)
    dispcount = intval.value
    print('num displays =', dispcount)

    displays = (screen_display_t * dispcount)()
    # get ref to displays
    rc = screen_get_context_property_pv(screen.screen_ctx,
        SCREEN_PROPERTY_DISPLAYS, cast(byref(displays), POINTER(c_void_p)))
    if rc: raise RuntimeError(rc)

    for i in range(dispcount):
        disp = displays[i]
        print('display #%d' % i, disp)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_DETACHABLE, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  detachable?', bool(intval))

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_ATTACHED, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  attached?', bool(intval))

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_FORMAT_COUNT, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  num formats', intval.value)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_ROTATION, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  rotation', intval.value)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_MIRROR_MODE, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  mirror mode?', intval.value)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_POWER_MODE, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  power mode', intval.value)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_KEEP_AWAKES, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  num keep awakes', intval.value)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_ID, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  id', intval.value)

        charval = create_string_buffer(50)
        rc = screen_get_display_property_cv(disp, SCREEN_PROPERTY_ID_STRING, len(charval), charval)
        if rc: raise RuntimeError(rc)
        print('  id string', charval.value)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_MODE_COUNT, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  num modes', intval.value)

    time.sleep(1)


# EOF
