'''Demonstrate/test loading font with FreeType and drawing onscreen.'''

import sys
import os
import math
import datetime
import time
import random
from ctypes import byref, cast, sizeof, c_int, c_void_p, c_ulong, POINTER
void_pp = POINTER(c_void_p)

import freetype

from bbxpy.wrapped.screen import *
from bbxpy.image import Image
import bbxrun


IMAGE_PATH = b'app/python/scripts/logo.png'
DEFAULT_SIZE = 24


def run():
    screen = bbxrun.screen
    screen.fill_screen(0x337733)

    xpos = 20
    image = Image(screen.screen_ctx)
    image.load(IMAGE_PATH)
    image.draw(xpos, 15, screen.screen_buf, scale=1/4)

    color = 0xff5511
    fontsize = 48
    leading = 70
    ypos = 200
    for text in [
        'BBX-Python!',
        'The time is %s' % datetime.datetime.now(),
        'Python ' + sys.version.split('\n', 1)[0],
        'Visit http://microcode.ca/bbx-python/ to learn more.',
        ]:
        draw_text(xpos, ypos, text, fontsize=fontsize, color=color)
        ypos += leading
        fontsize = 36
        color = 0xffffff

    time.sleep(3)


def draw_text(xpos, ypos, render_text, fontsize=DEFAULT_SIZE, color=0xffffff):
    screen = bbxrun.screen

    #----------------------------------
    # load font and render chars
    face = freetype.Face('/usr/fonts/font_repository/ttf-bitstream-vera-1.10/VeraSe.ttf')
    face.set_char_size(fontsize * 64)
    metrics = face.size
    #~ print('size', [x for x in dir(face.size) if not x.startswith('__')])
    #~ size ['_FT_Size_Metrics', 'ascender', 'descender', 'height', 'max_advance', 'x_ppem',
    #~ 'x_scale', 'y_ppem', 'y_scale']
    print('face', metrics.x_ppem, metrics.y_ppem, face.units_per_EM)
    bbox = face.bbox
    print('bbox', bbox.xMin, bbox.yMin, bbox.xMax, bbox.yMax)
    bufwidth = int(math.ceil((bbox.xMax - bbox.xMin) / face.units_per_EM * metrics.x_ppem) + 1)
    bufheight = int(math.ceil((bbox.yMax - bbox.yMin) / face.units_per_EM * metrics.y_ppem) + 1)
    print('buf size', bufwidth, bufheight)

    face.load_char('n')
    space_width = int(face.glyph.bitmap.width * 0.75)
    print('space width', space_width)

    #----------------------------------
    # prepare pixmap and buffer to draw into
    pixmap = screen_pixmap_t()
    rc = screen_create_pixmap(byref(pixmap), screen.screen_ctx)
    if rc: raise RuntimeError(rc)

    # set format to byte-per-pixel to match FreeType buffers?
    format = c_int(SCREEN_FORMAT_RGBA8888)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_FORMAT, byref(format))
    if rc: raise RuntimeError(rc)

    # set up pixmap buffer for NATIVE usage so we can blit from it
    usage = c_int(SCREEN_USAGE_NATIVE | SCREEN_USAGE_WRITE)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_USAGE, byref(usage))
    #~ print('screen_set_pixmap_property_iv', rc)
    if rc: raise RuntimeError(rc)

    # set size for buffer based on glyph bitmap size
    size = (c_int * 2)(bufwidth, bufheight)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_BUFFER_SIZE, cast(byref(size), POINTER(c_int)))
    if rc: raise RuntimeError(rc)

    # create buffer for pixmap
    rc = screen_create_pixmap_buffer(pixmap)
    print('screen_create_pixmap_buffer', rc)
    if rc: raise RuntimeError(rc)

    # retrieve buffer reference from pixmap
    pixbuf = screen_buffer_t()
    rc = screen_get_pixmap_property_pv(pixmap, SCREEN_PROPERTY_RENDER_BUFFERS, cast(byref(pixbuf), void_pp))
    if rc: raise RuntimeError(rc)

    # sanity check size of buffer: can remove code later
    size = (c_int * 2)()
    rc = screen_get_buffer_property_iv(pixbuf, SCREEN_PROPERTY_BUFFER_SIZE, cast(byref(size), POINTER(c_int)))
    if rc: raise RuntimeError(rc)
    print('check pixbuf, size', size[0], size[1])

    #----------------------------------
    # draw glyphs into the pixmap's buffer

    dataaddr = c_void_p()
    rc = screen_get_buffer_property_pv(pixbuf, SCREEN_PROPERTY_POINTER, cast(byref(dataaddr), void_pp))
    print('screen_get_buffer_property_pv', rc)
    if rc: raise RuntimeError(rc)
    print('pointer', dataaddr.value)

    bufdata = cast(dataaddr, POINTER(c_ulong))
    print('budata', bufdata, bufdata[0], bufdata[1], bufdata[2])

    stride_val = c_int()
    rc = screen_get_buffer_property_iv(pixbuf, SCREEN_PROPERTY_STRIDE, byref(stride_val))
    if rc: raise RuntimeError(rc)
    stride = stride_val.value
    print('stride', stride)

    for char in render_text:
        face.load_char(char)
        g = face.glyph
        print('glyph %r @(%s,%s):' % (char, xpos, ypos), g.bitmap_left, g.bitmap_top,
            math.ceil(g.advance.x // 26.6), math.ceil(g.advance.y // 26.6),
            int(g.linearHoriAdvance // 16.16), int(g.linearVertAdvance // 16.16))
        bitmap = face.glyph.bitmap
        print('   bitmap:', bitmap.width, bitmap.rows, bitmap.num_grays, bitmap.pitch, bitmap.pixel_mode, len(bitmap.buffer))
        if bitmap.width and bitmap.rows:
            render_bitmap(bitmap, bufdata, stride, color)
            blit_buffer(bufdata, bitmap, screen, pixbuf, xpos, ypos - g.bitmap_top)
            xpos += bitmap.width + g.bitmap_left + 1
        else:
            xpos += space_width

    rect = (c_int * 4)()
    rc = screen_get_window_property_iv(screen.screen_win, SCREEN_PROPERTY_BUFFER_SIZE,
        cast(byref(rect, 2 * sizeof(c_int)), POINTER(c_int)))
    print('rect', list(rect))
    if rc: raise RuntimeError(rc)

    rc = screen_post_window(screen.screen_win, screen.screen_buf, 1, rect, 0)
    if rc: raise RuntimeError(rc)


def render_bitmap(bitmap, bufdata, stride, color):
    # access buffer's pointer and transfer glyph data over
    rowstart = 0
    offset = 0
    col = 0
    for pixdata in bitmap.buffer:
        bufdata[rowstart + offset] = (pixdata << 24) | color;
        offset += 1
        col += 1
        if col >= bitmap.width:
            col = 0
            rowstart += stride // sizeof(bufdata._type_)
            offset = 0

    #~ print('sanity', rowstart, offset, col)


def blit_buffer(bufdata, bitmap, screen, pixbuf, x, y):
    #----------------------------------
    # prepare window to receive image in blit
    screen_buf = screen.screen_buf

    if x < 0 or x >= 1024 or y < 0 or y >= 600:
        return

    width = bitmap.width
    if x + width >= 1024:
        width = 1024 - x

    height = bitmap.rows
    if y + height >= 600:
        height = 600 - y
    print('blit', x, y, bitmap.width, bitmap.rows, width, height)

    if not width or not height:
        return

    hg = [
        SCREEN_BLIT_SOURCE_WIDTH, width,
        SCREEN_BLIT_SOURCE_HEIGHT, height,
        SCREEN_BLIT_DESTINATION_X, x,
        SCREEN_BLIT_DESTINATION_Y, y,
        SCREEN_BLIT_DESTINATION_WIDTH, width,
        SCREEN_BLIT_DESTINATION_HEIGHT, height,
        SCREEN_BLIT_TRANSPARENCY, SCREEN_TRANSPARENCY_SOURCE_OVER,
        SCREEN_BLIT_END
        ]
    hg = (c_int * len(hg))(*hg)
    rc = screen_blit(screen.screen_ctx, screen_buf, pixbuf, hg)
    if rc: raise RuntimeError(rc)
    #~ print('screen_blit', rc)

    rc = screen_flush_blits(screen.screen_ctx, 0)
    if rc: raise RuntimeError(rc)


# EOF
