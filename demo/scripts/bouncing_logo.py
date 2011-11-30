'''Demonstrate bouncing the logo around the screen.'''

import time
import random
import math
import threading
from ctypes import byref, cast, sizeof, c_int, POINTER

from bbxpy.wrapped.screen import *
from bbxpy.wrapped.img import *
from bbxpy.image import Image

IMAGE_PATH = b'app/python/scripts/logo.png'
WAV_FILE = 'app/python/scripts/bounce.wav'

from qnx import audio

_sound_thread = None

def sound():
    _sound_event.set()

def _sound_thread_run():
    player = audio.AudioPlayer()
    while 1:
        _sound_event.wait()
        _sound_event.clear() # race condition possible... forgot proper technique at 2:21am
        player.play(WAV_FILE)


def run():
    import bbxrun
    screen = bbxrun.screen

    global _sound_thread, _sound_event
    if not _sound_thread:
        _sound_thread = threading.Thread(target=_sound_thread_run)
        _sound_thread.daemon = True
        _sound_event = threading.Event()
        _sound_thread.start()

    image = Image(screen.screen_ctx)
    image.load(IMAGE_PATH)

    # find size of window
    rect = (c_int * 4)()
    rc = screen_get_window_property_iv(screen.screen_win, SCREEN_PROPERTY_BUFFER_SIZE,
        cast(byref(rect, 2 * sizeof(c_int)), POINTER(c_int)))
    print('rect', list(rect))
    if rc: raise RuntimeError(rc)

    start = time.time()
    framecount = 0
    scale = 1/4
    DURATION = 10.0

    xmin = 0
    xmax = rect[2] - int(image.width * scale)
    ymin = 50
    ymax = rect[3] - int(image.height * scale)

    x = 0
    y = ymin

    vx = 15
    #~ gravity = 9.98
    GFACTOR = 70

    timebase = start
    while time.time() - start < DURATION:
        screen.fill_screen(0xff0000ff)
        image.draw(x, ymax if y > ymax else y, screen.screen_buf, scale=scale)

        rc = screen_post_window(screen.screen_win, screen.screen_buf, 1, rect, 0)
        if rc: raise RuntimeError(rc)
        framecount += 1

        # update based on current values
        x += vx

        # account for physics
        elapsed = time.time() - timebase

        delta = math.pow(abs(elapsed) * GFACTOR, 2)
        #~ print('> %.3fs: %d pow %.1f %.1f' % (elapsed, y, elapsed * gravity, delta))
        y = ymin + delta

        if x > xmax:
            x = xmax - (x - xmax)
            vx = -vx

        elif x < xmin:
            x = xmin + (xmin - x)
            vx = -vx

        if y > ymax and elapsed > 0:
            timebase += elapsed * 2
            sound()

    print('fps=%.1f' % (framecount / DURATION))


# EOF
