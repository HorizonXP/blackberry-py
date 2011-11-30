'''Image class to load and render bitmaps.'''

from ctypes import byref, cast, c_int, c_void_p, POINTER
void_pp = POINTER(c_void_p)

from bbxpy.wrapped.screen import *
from bbxpy.wrapped.img import *

__all__ = ['Image']


class Image:
    def __init__(self, context):
        self._context = context
        self._pixmap = None


    def load(self, path):
        ilib = img_lib_t()
        rc = img_lib_attach(byref(ilib))
        if rc: raise RuntimeError(rc)

        img = img_t()

        # 24-bits/pixel BGR format, little-endian
        img.format = IMG_FMT_PKLE_XRGB8888
        img.flags |= IMG_FORMAT

        # set up decoder to load image into new pixmap
        self._pixmap = screen_pixmap_t()
        rc = screen_create_pixmap(byref(self._pixmap), self._context)
        if rc: raise RuntimeError(rc)

        callouts = img_decode_callouts_t()
        callouts.setup_f = decode_setup
        callouts.abort_f = decode_abort
        callouts.data = cast(self._pixmap, POINTER(c_uint))

        rc = img_load_file(ilib, path, byref(callouts), byref(img))
        if rc: raise RuntimeError(rc)
        #~ print('img_load_file', rc)
        #~ print('img is %d x %d x %d' % (img.w, img.h, IMG_FMT_BPP(img.format)))

        self.width = img.w
        self.height = img.h

        img_lib_detach(ilib)


    def draw(self, x, y, buffer, scale=1.0):
        pixbuf = screen_buffer_t()
        rc = screen_get_pixmap_property_pv(self._pixmap, SCREEN_PROPERTY_RENDER_BUFFERS,
            cast(byref(pixbuf), void_pp))
        if rc: raise RuntimeError(rc)

        # prepare window to receive image in blit
        hg = [
            SCREEN_BLIT_SOURCE_WIDTH, self.width,
            SCREEN_BLIT_SOURCE_HEIGHT, self.height,
            SCREEN_BLIT_DESTINATION_X, x,
            SCREEN_BLIT_DESTINATION_Y, y,
            SCREEN_BLIT_DESTINATION_WIDTH, int(self.width * scale),
            SCREEN_BLIT_DESTINATION_HEIGHT, int(self.height * scale),
            SCREEN_BLIT_TRANSPARENCY, SCREEN_TRANSPARENCY_SOURCE_OVER,
            SCREEN_BLIT_END
            ]
        hg = (c_int * len(hg))(*hg)

        rc = screen_blit(self._context, buffer, pixbuf, hg)
        if rc: raise RuntimeError(rc)


#~ img_decode_setup_f = CFUNCTYPE(c_int, POINTER(c_uint), POINTER(img_t), c_uint)
#~ static int decode_setup(uintptr_t data, img_t *img, unsigned flags):
def decode_setup(data, img, flags):
    pixmap = cast(data, screen_pixmap_t)
    buffer = screen_buffer_t()

    # set up pixmap buffer for NATIVE usage so we can blit from it
    usage = c_int(SCREEN_USAGE_NATIVE)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_USAGE, byref(usage))
    #~ print('screen_set_pixmap_property_iv', rc)
    if rc: raise RuntimeError(rc)

    img = img.contents
    size = (c_int * 2)(img.w, img.h)
    print('decode: image size', img.w, img.h)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_BUFFER_SIZE,
        cast(byref(size), POINTER(c_int)))
    if rc: raise RuntimeError(rc)

    # set format to have alpha channel for our blitting
    format = c_int(SCREEN_FORMAT_RGBA8888)
    rc = screen_set_pixmap_property_iv(pixmap, SCREEN_PROPERTY_FORMAT, byref(format))
    if rc: raise RuntimeError(rc)

    rc = screen_create_pixmap_buffer(pixmap)
    #~ print('screen_create_pixmap_buffer', rc)
    if rc: raise RuntimeError(rc)

    rc = screen_get_pixmap_property_pv(pixmap, SCREEN_PROPERTY_RENDER_BUFFERS,
        cast(byref(buffer), void_pp))
    #~ print('screen_get_pixmap_property_pv', rc)
    if rc: raise RuntimeError(rc)

    rc = screen_get_buffer_property_pv(buffer, SCREEN_PROPERTY_POINTER,
        cast(byref(img.access.direct.data), void_pp))
    #~ print('screen_get_buffer_property_pv', rc)
    if rc: raise RuntimeError(rc)

    # could use something like offset = img_t.access.offset + img_t.access.direct.offset + img_t.access.direct.stride.offset
    # then cast(byref(img, offset), POINTER(c_int))
    stride_val = c_int()
    rc = screen_get_buffer_property_iv(buffer, SCREEN_PROPERTY_STRIDE, byref(stride_val))
    if rc: raise RuntimeError(rc)

    img.access.direct.stride = stride_val.value
    #~ print('stride', stride_val)

    img.flags |= IMG_DIRECT
    return IMG_ERR_OK

decode_setup = img_decode_setup_f(decode_setup)


#~ img_decode_abort_f = CFUNCTYPE(None, POINTER(c_uint), POINTER(img_t))
def decode_abort(data, img):
    #~ print('decode_abort')
    pixmap = cast(data, screen_pixmap_t)
    rc = screen_destroy_pixmap_buffer(pixmap)
    if rc: raise RuntimeError(rc)

decode_abort = img_decode_abort_f(decode_abort)


# EOF
