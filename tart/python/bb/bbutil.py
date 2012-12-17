
from ctypes import (byref, c_int, cast, c_void_p, c_float)

from ._wrap import _func, _register_funcs
from .egl import *
from . import gles

egl_disp = EGLDisplay()
egl_surf = EGLSurface()

egl_conf = EGLConfig()
egl_ctx = EGLContext()

initialized = 0

SWAP_INTERVAL = 1


#-----------------------------------------------
#
ERRMSG = [
    "function succeeded",
    "EGL is not initialized, or could not be initialized, for the specified display",
    "cannot access a requested resource",
    "failed to allocate resources for the requested operation",
    "an unrecognized attribute or attribute value was passed in an attribute list",
    "an EGLConfig argument does not name a valid EGLConfig",
    "an EGLContext argument does not name a valid EGLContext",
    "the current surface of the calling thread is no longer valid",
    "an EGLDisplay argument does not name a valid EGLDisplay",
    "arguments are inconsistent",
    "an EGLNativePixmapType argument does not refer to a valid native pixmap",
    "an EGLNativeWindowType argument does not refer to a valid native window",
    "one or more argument values are invalid",
    "an EGLSurface argument does not name a valid surface configured for rendering",
    "a power management event has occurred",
    "unknown error code",
    ]


def bbutil_egl_perror(msg):
    i = eglGetError() - EGL_SUCCESS

    if i < 0 or i >= len(ERRMSG):
        i = len(ERRMSG) - 1

    print('{}: 0x{:04x} {}'.format(msg, i + EGL_SUCCESS, ERRMSG[i]))


#-----------------------------------------------
#
def bbutil_init_egl(screen_win):
    print('bbutil_init_egl', screen_win, bool(screen_win), cast(screen_win, c_void_p).value)

    def make_array(type, data):
        array_type = type * len(data)
        return array_type(*data)

    attrib_list = make_array(EGLint, [
        EGL_RED_SIZE,        8,
        EGL_GREEN_SIZE,      8,
        EGL_BLUE_SIZE,       8,
        EGL_ALPHA_SIZE,      8,
        EGL_SURFACE_TYPE,    EGL_WINDOW_BIT,
        EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
        EGL_NONE,
        ])
    attributes = make_array(EGLint, [EGL_CONTEXT_CLIENT_VERSION, 2, EGL_NONE])

    egl_disp.value = eglGetDisplay(EGL_DEFAULT_DISPLAY)
    if not egl_disp:
        bbutil_egl_perror("eglGetDisplay")
        bbutil_terminate()
        raise Exception()
    print('eglGetDisplay', egl_disp.value)
    c_int.in_dll(dll, 'egl_disp').value = egl_disp.value

    major = c_int()
    minor = c_int()
    rc = eglInitialize(egl_disp, byref(major), byref(minor))
    if rc != EGL_TRUE:
        bbutil_egl_perror("eglInitialize")
        bbutil_terminate()
        raise Exception()
    print("EGL v%d.%d" % (major.value, minor.value))   # v1.4

    # acquires per-thread resources
    rc = eglBindAPI(EGL_OPENGL_ES_API)
    if rc != EGL_TRUE:
        bbutil_egl_perror("eglBindApi")
        bbutil_terminate()
        raise Exception()

    num_configs = c_int()
    if not eglChooseConfig(egl_disp, attrib_list, byref(egl_conf), 1, byref(num_configs)):
        bbutil_terminate()
        raise Exception()

    egl_ctx.value = eglCreateContext(egl_disp, egl_conf, EGL_NO_CONTEXT, attributes)
    if not egl_ctx:
        bbutil_egl_perror("eglCreateContext")
        bbutil_terminate()
        raise Exception()
    print('eglCreateContext', egl_ctx.value)

    egl_surf.value = eglCreateWindowSurface(egl_disp, egl_conf, screen_win, None)
    if not egl_surf:
        bbutil_egl_perror("eglCreateWindowSurface")
        bbutil_terminate()
        raise Exception()
    print('eglCreateWindowSurface', egl_surf.value)
    c_int.in_dll(dll, 'egl_surf').value = egl_surf.value

    rc = eglMakeCurrent(egl_disp, egl_surf, egl_surf, egl_ctx)
    if rc != EGL_TRUE:
        bbutil_egl_perror("eglMakeCurrent")
        bbutil_terminate()
        raise Exception()

    rc = eglSwapInterval(egl_disp, SWAP_INTERVAL)
    if rc != EGL_TRUE:
        bbutil_egl_perror("eglSwapInterval")
        bbutil_terminate()
        raise Exception()

    global initialized
    initialized = 1

    c_int.in_dll(dll, 'initialized').value = 1


#-----------------------------------------------
#
def bbutil_terminate(chart):
    # typical EGL cleanup
    if egl_disp:
        eglMakeCurrent(egl_disp, EGL_NO_SURFACE, EGL_NO_SURFACE, EGL_NO_CONTEXT)
        if egl_surf:
            eglDestroySurface(egl_disp, egl_surf)
            egl_surf.value = EGL_NO_SURFACE.value

        if egl_ctx.value:
            eglDestroyContext(egl_disp, egl_ctx)
            egl_ctx.value = EGL_NO_CONTEXT.value

        import chart as c
        c.destroy_window(chart)

        eglTerminate(egl_disp)
        egl_disp.value = EGL_NO_DISPLAY.value

    eglReleaseThread()

    global initialized
    initialized = 0


#-----------------------------------------------
#
def bbutil_swap():
    rc = eglSwapBuffers(egl_disp, egl_surf)
    if rc != EGL_TRUE:
        print('egl_disp', egl_disp.value, 'egl_surf', egl_surf.value)
        bbutil_egl_perror("eglSwapBuffers")
        raise Exception()



#-----------------------------------------------
#
# int bbutil_calculate_dpi(screen_display_t screen_disp) {
#     int rc;
#     int screen_phys_size[2];

#     rc = screen_get_display_property_iv(screen_disp, SCREEN_PROPERTY_PHYSICAL_SIZE, screen_phys_size);
#     if (rc) {
#         perror("screen_get_display_property_iv");
#         bbutil_terminate();
#         return EXIT_FAILURE;
#     }

#     //Simulator will return 0,0 for physical size of the screen, so use default dpi
#     if ((screen_phys_size[0] == 0) && (screen_phys_size[1] == 0)) {
#         return 356; // dev alpha, 1280x768
#     } else {
#         int screen_resolution[2];
#         rc = screen_get_display_property_iv(screen_disp, SCREEN_PROPERTY_SIZE, screen_resolution);
#         if (rc) {
#             perror("screen_get_display_property_iv");
#             bbutil_terminate();
#             return EXIT_FAILURE;
#         }
#         double diagonal_pixels = sqrt(
#               screen_resolution[0] * screen_resolution[0]
#             + screen_resolution[1] * screen_resolution[1]);
#         double diagonal_inches = 0.0393700787 * sqrt(
#               screen_phys_size[0] * screen_phys_size[0]
#             + screen_phys_size[1] * screen_phys_size[1]);
#         return (int)(diagonal_pixels / diagonal_inches + 0.5);
#     }
# }


class Font:
    # https://developer.blackberry.com/devzone/design/devices_and_screen_sizes.html
    dpi = int(round(25.4 / 0.07125))
    DEFAULT_SIZE = 16

    __cache = {}

    def __init__(self, path, point_size=DEFAULT_SIZE):
        if not self.dpi:
            raise Exception('Font.dpi must be set before creating fonts')

        if point_size > 28:
            print('Warning: sizes above 28 may not be supported')

        self.font = bbutil_load_font(path.encode('ascii', 'ignore'), point_size, self.dpi)
        print('font', self.font, cast(self.font, c_void_p).value)

        # cache for easier reuse
        self.__cache[path, point_size] = self


    @classmethod
    def get_font(cls, path, point_size=DEFAULT_SIZE):
        try:
            return cls.__cache[path, point_size]
        except KeyError:
            return Font(path, point_size)


    def measure(self, text):
        text = text.encode('ascii', 'replace')
        w = c_float()
        h = c_float()
        bbutil_measure_text(self.font, text, byref(w), byref(h))
        return w.value, h.value


    def render(self, text, x, y, color, rotation=0):
        text = text.encode('ascii', 'replace')
        # print('render', text, x, y, color)
        bbutil_render_text(self.font, text, x, y, -rotation, *color)


class font_t(Structure):
    _fields_ = []

bbutil_load_font = _func(POINTER(font_t), c_char_p, c_int, c_int)
bbutil_destroy_font = _func(None, POINTER(font_t))
bbutil_measure_text = _func(None, POINTER(font_t), c_char_p,
    POINTER(c_float), POINTER(c_float))
bbutil_render_text = _func(None, POINTER(font_t), c_char_p, c_float, c_float,
    c_float, c_float, c_float, c_float, c_float)

#----------------------------
# apply argtypes/restype to all functions
#
dll = _register_funcs('/accounts/1000/shared/misc/BatteryGuru/_chart.so', globals())
dll.init()


# EOF
