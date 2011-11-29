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
        print('display #%d' % i) # , disp)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_DETACHABLE, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  detachable?', bool(intval))

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_ATTACHED, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  attached?', bool(intval))

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_FORMAT_COUNT, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  num formats', intval.value)

        formats = (c_int * intval.value)()
        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_FORMATS, formats)
        if rc: raise RuntimeError(rc)
        print('  formats', list(formats))

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_ROTATION, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  rotation', intval.value)

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_GAMMA, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  gamma', intval.value)

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

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_TYPE, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  type', intval.value)

        psize = (c_int * 2)()
        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_PHYSICAL_SIZE, cast(byref(psize), POINTER(c_int)))
        if rc: raise RuntimeError(rc)
        print('  physical size', psize[0], psize[1])

        size = (c_int * 2)()
        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_SIZE, cast(byref(size), POINTER(c_int)))
        if rc: raise RuntimeError(rc)
        print('  resolution', size[0], size[1])

        try:
            pitch = psize[0] / size[0]
            print('  pixel size %.2fmm (%.1fdpi)' % (pitch, 25.4/pitch))
        except:
            pass

        rc = screen_get_display_property_iv(disp, SCREEN_PROPERTY_MODE_COUNT, byref(intval))
        if rc: raise RuntimeError(rc)
        print('  num modes', intval.value)
        modecount = intval.value

        modes = (screen_display_mode_t * modecount)()

        # get ref to modes
        rc = screen_get_display_modes(disp, len(modes), modes)
        if rc: raise RuntimeError(rc)

        for j in range(modecount):
            mode = modes[j]
            if not mode:
                print('    mode #%d:' % j, '(null)')
                continue

            print('    mode #%s: %s x %s @%sHz, interlaced? %s, index %s, flags %s, aspect_ratio %s/%s' %
                (j, mode.width, mode.height, mode.refresh, mode.interlaced, mode.index, mode.flags,
                mode.aspect_ratio[0], mode.aspect_ratio[1]))

    time.sleep(1)


# EOF
