'''Demonstrate/test loading image file and blitting to screen.'''

import sys
import os
import time
import random
from ctypes import byref, cast, sizeof, c_int, c_void_p, pointer

from bbxpy.wrapped.screen import *
from bbxpy.wrapped.img import *

def showptr(p):
    return p.contents if p else 'NULL'


def run():
    import bbxrun
    screen = bbxrun.screen

    ilib = img_lib_t()
    rc = img_lib_attach(byref(ilib))
    print('img_lib_attach', rc)
    if rc: raise RuntimeError(rc)

    img = img_t()

    # 24-bits/pixel BGR format, little-endian
    img.format = IMG_FMT_PKLE_XRGB8888
    img.flags |= IMG_FORMAT

    # set up decoder to load image into new pixmap
    pixmap = screen_pixmap_t()
    rc = screen_create_pixmap(byref(pixmap), screen.screen_ctx)
    print('screen_create_pixmap', rc)
    if rc: raise RuntimeError(rc)

    callouts = img_decode_callouts_t()
    callouts.setup_f = decode_setup
    callouts.abort_f = decode_abort
    callouts.data = cast(pixmap, POINTER(c_uint))

    rc = img_load_file(ilib, b'shared/documents/scripts/logo.png', byref(callouts), byref(img))
    if rc: raise RuntimeError(rc)
    #~ print('img_load_file', rc)
    #~ print('img is %d x %d x %d' % (img.w, img.h, IMG_FMT_BPP(img.format)))

    pixbuf = screen_buffer_t()
    void_pp = POINTER(c_void_p)
    rc = screen_get_pixmap_property_pv(pixmap, SCREEN_PROPERTY_RENDER_BUFFERS, cast(byref(pixbuf), void_pp))
    if rc: raise RuntimeError(rc)

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
        hg = [
            SCREEN_BLIT_SOURCE_WIDTH, img.w,
            SCREEN_BLIT_SOURCE_HEIGHT, img.h,
            SCREEN_BLIT_DESTINATION_X, random.randint(0, rect[2] - int(img.w * scale)),
            SCREEN_BLIT_DESTINATION_Y, random.randint(0, rect[3] - int(img.h * scale)),
            SCREEN_BLIT_DESTINATION_WIDTH, int(img.w * scale),
            SCREEN_BLIT_DESTINATION_HEIGHT, int(img.h * scale),
            SCREEN_BLIT_TRANSPARENCY, SCREEN_TRANSPARENCY_SOURCE_OVER,
            SCREEN_BLIT_END
            ]
        hg = (c_int * len(hg))(*hg)

        rc = screen_blit(screen.screen_ctx, screen_buf, pixbuf, hg)
        if rc: raise RuntimeError(rc)
        blits += 1
        #~ print('screen_blit', rc)

        # max refresh rate 60Hz
        if time.time() - prev >= 1/60:
            prev = time.time()
            rc = screen_post_window(screen.screen_win, screen_buf, 1, rect, 0)
            if rc: raise RuntimeError(rc)
            posts += 1

    print('blits=%s posts=%s fps=%.1f' % (blits, posts, posts / DURATION))

    img_lib_detach(ilib)

    time.sleep(1)


#~ img_decode_setup_f = CFUNCTYPE(c_int, POINTER(c_uint), POINTER(img_t), c_uint)
#~ static int decode_setup(uintptr_t data, img_t *img, unsigned flags):
def decode_setup(data, img, flags):
    pixmap = cast(data, screen_pixmap_t)
    buffer = screen_buffer_t()
    size = (c_int * 2)()

    # set up pixmap buffer for NATIVE usage so we can blit from it
    usage = c_int(SCREEN_USAGE_NATIVE)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_USAGE, byref(usage))
    #~ print('screen_set_pixmap_property_iv', rc)
    if rc: raise RuntimeError(rc)

    img = img.contents
    size[0] = img.w
    size[1] = img.h
    print('decode: image size', img.w, img.h)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_BUFFER_SIZE, cast(byref(size), POINTER(c_int)))
    if rc: raise RuntimeError(rc)

    # set format to have alpha channel for our blitting
    format = c_int(SCREEN_FORMAT_RGBA8888)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_FORMAT, byref(format))
    if rc: raise RuntimeError(rc)

    rc = screen_create_pixmap_buffer(pixmap)
    print('screen_create_pixmap_buffer', rc)
    if rc: raise RuntimeError(rc)

    void_pp = POINTER(c_void_p)
    rc = screen_get_pixmap_property_pv(pixmap, SCREEN_PROPERTY_RENDER_BUFFERS, cast(byref(buffer), void_pp))
    #~ print('screen_get_pixmap_property_pv', rc)
    if rc: raise RuntimeError(rc)

    rc = screen_get_buffer_property_pv(buffer, SCREEN_PROPERTY_POINTER, cast(byref(img.access.direct.data), void_pp))
    #~ print('screen_get_buffer_property_pv', rc)
    if rc: raise RuntimeError(rc)

    # could use something like offset = img_t.access.offset + img_t.access.direct.offset + img_t.access.direct.stride.offset
    # then cast(byref(img, offset), POINTER(c_int))
    stride_val = c_int()
    rc = screen_get_buffer_property_iv(buffer, SCREEN_PROPERTY_STRIDE, byref(stride_val))
    if rc: raise RuntimeError(rc)

    img.access.direct.stride = stride_val.value
    print('stride', stride_val)

    img.flags |= IMG_DIRECT
    return IMG_ERR_OK

decode_setup = img_decode_setup_f(decode_setup)


#~ img_decode_abort_f = CFUNCTYPE(None, POINTER(c_uint), POINTER(img_t))
def decode_abort(data, img):
    print('decode_abort')
    pixmap = cast(data, screen_pixmap_t)
    rc = screen_destroy_pixmap_buffer(pixmap)
    if rc: raise RuntimeError(rc)

decode_abort = img_decode_abort_f(decode_abort)

# EOF
