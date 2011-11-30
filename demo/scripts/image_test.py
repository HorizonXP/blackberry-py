'''Demonstrate/test loading image file and blitting to screen.'''

import time
import random
from ctypes import byref, cast, sizeof, c_int, POINTER

from bbxpy.wrapped.screen import *
from bbxpy.wrapped.img import *
from bbxpy.image import Image

IMAGE_PATH = b'app/python/scripts/logo.png'


def run():
    import bbxrun
    screen = bbxrun.screen

    image = Image(screen.screen_ctx)
    image.load(IMAGE_PATH)

    # prepare window to receive image in blit
    screen_buf = screen.screen_buf

    rect = (c_int * 4)()
    rc = screen_get_window_property_iv(screen.screen_win, SCREEN_PROPERTY_BUFFER_SIZE,
        cast(byref(rect, 2 * sizeof(c_int)), POINTER(c_int)))
    print('rect', list(rect))
    if rc: raise RuntimeError(rc)

    start = time.time()
    prev = time.time()
    blits = posts = 0
    scale = 1/4
    DURATION = 3.5
    while time.time() - start < DURATION:
        x = random.randint(0, rect[2] - int(image.width * scale))
        y = random.randint(0, rect[3] - int(image.height * scale))
        image.draw(x, y, screen_buf, scale=scale)

        blits += 1

        # max refresh rate 60Hz
        if time.time() - prev >= 1/60:
            prev = time.time()
            rc = screen_post_window(screen.screen_win, screen_buf, 1, rect, 0)
            if rc: raise RuntimeError(rc)
            posts += 1

    print('blits=%s posts=%s fps=%.1f' % (blits, posts, posts / DURATION))


# EOF
