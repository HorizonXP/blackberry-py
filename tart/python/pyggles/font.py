
import os
from ctypes import (byref, c_int, cast, c_void_p, c_float, c_char_p,
    Structure, POINTER, pointer)
import traceback

from bb._wrap import _func, _register_funcs
from bb.egl import EGLDisplay, EGLSurface
from bb.gles import GLuint, glDeleteTextures, glDeleteProgram
from .drawing import _dll
from .color import Color
from . import shaders, context
from tart.util import counter_id


class FontError(Exception):
    '''Indicates an error loading or using a font.'''


SYS_FONTS = '/usr/fonts/font_repository/monotype'


SHADER_VERT = '''\
precision mediump float;
uniform mat4 u_transform;
attribute vec2 a_position;
attribute vec2 a_texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = u_transform * vec4(a_position, 0.0, 1.0);
    v_texcoord = a_texcoord;
}
'''

SHADER_FRAG = '''\
precision lowp float;
varying vec2 v_texcoord;
uniform sampler2D u_texture;
uniform vec4 u_color;
void main()
{
    vec4 temp = texture2D(u_texture, v_texcoord);
    gl_FragColor = u_color * temp;
}
'''


FONT_CHARS = 128

class Font(Structure):
    '''Per-font info used for rendering a particular font.'''
    _fields_ = [
        ('pt', c_float),
        ('texture_id', GLuint),
        ('advance', c_float * FONT_CHARS),
        ('width', c_float * FONT_CHARS),
        ('height', c_float * FONT_CHARS),
        ('tex_x1', c_float * FONT_CHARS),
        ('tex_x2', c_float * FONT_CHARS),
        ('tex_y1', c_float * FONT_CHARS),
        ('tex_y2', c_float * FONT_CHARS),
        ('offset_x', c_float * FONT_CHARS),
        ('offset_y', c_float * FONT_CHARS),
        ]


    # https://developer.blackberry.com/devzone/design/devices_and_screen_sizes.html
    dpi = int(round(25.4 / 0.07125))
    DEFAULT_SIZE = 16


    def __init__(self, path, point_size=DEFAULT_SIZE):
        self._id = counter_id()
        self.name = (os.path.splitext(os.path.basename(path))[0] + ' ' + str(point_size)).title()

        # print('Font.__init__', self, point_size, path)

        _orig_path = path
        if not self.dpi:
            raise Exception('Font.dpi must be set before creating fonts')

        if point_size > 28:
            print('Warning: sizes above 28 may not be supported')

        if not os.path.isfile(path):
            trypath = os.path.join(SYS_FONTS, path)
            if os.path.isfile(trypath):
                path = trypath

        rc = font_load(self, path.encode('ascii', 'ignore'), point_size, self.dpi)
        if rc:
            raise FontError('font_load returned %s' % rc)
        # print('texture_id', self.texture_id)

        # print('font', _orig_path, point_size)


    def __del__(self):
        # print('!!! __del__ Font', self)

        try:
            if self.texture_id:
                # print('texture_id', self.texture_id)
                _ids = (GLuint * 1)(self.texture_id)
                glDeleteTextures(1, cast(_ids, POINTER(GLuint)))
                self.texture_id = 0
        except:
            traceback.print_exc()


    def __repr__(self):
        return '<Font @%s %s>' % (self._id, self.name)


    @classmethod
    def get_font(cls, path, point_size=DEFAULT_SIZE):
        # print('get_font', path, point_size)
        try:
            cache = context.font_cache
            # print('reusing context.font_cache')
        except AttributeError:
            # print('create new context.font_cache')
            cache = context.font_cache = {}

        try:
            font = cache[path, point_size]
            # print('found font in cache', font)
        except KeyError:
            font = cls(path, point_size)
            # print('created new font', font)

            # cache for easier reuse
            cache[path, point_size] = font

        return font


    def measure(self, text):
        text = text.encode('ascii', 'replace')
        w = c_float()
        h = c_float()
        font_measure_text(self, text, byref(w), byref(h))
        # print('measured', text, w.value, h.value)
        return w.value, h.value


    def render(self, text, x, y, color, rotation=0):
        support = FontSupport.context_cached()
        if isinstance(color, Color):
            color = color.tuple()
        text = text.encode('ascii', 'replace')
        # print('render', text, x, y, support.program, self.texture_id)
        font_render_text(support, self, text, x, y, -rotation, *color)



class FontSupport(Structure):
    '''Context-specific info used for rendering all fonts.'''
    _fields_ = [
        ('egl_disp', EGLDisplay),
        ('egl_surf', EGLSurface),
        ('program', GLuint),
        ('u_transform', GLuint),
        ('u_texture', GLuint),
        ('u_color', GLuint),
        ('a_position', GLuint),
        ('a_texcoord', GLuint),
        ]


    def __init__(self):
        # a bit of ugliness
        self.egl_disp = context.egl_disp
        self.egl_surf = context.egl_surf

        vs = shaders.Shader(SHADER_VERT)
        fs = shaders.Shader(SHADER_FRAG)
        prog = self._prog = shaders.Program(vs, fs, 'FontSupport')
        self.program = self._prog.handle

        # store the locations of the shader variables we need later
        self.u_transform = prog.uniform('u_transform')
        self.u_texture = prog.uniform('u_texture')
        self.u_color = prog.uniform('u_color')
        self.a_position = prog.attribute('a_position')
        self.a_texcoord = prog.attribute('a_texcoord')


    @classmethod
    def context_cached(cls):
        try:
            support = context.font_support
        except AttributeError:
            support = context.font_support = cls()

        return support



font_load = _func(c_int, POINTER(Font), c_char_p, c_int, c_int)
font_render_text = _func(None, POINTER(FontSupport), POINTER(Font),
    c_char_p, c_float, c_float,
    c_float, c_float, c_float, c_float, c_float)
font_measure_text = _func(None, POINTER(Font), c_char_p,
    POINTER(c_float), POINTER(c_float))


#----------------------------
# apply argtypes/restype to all functions
#
_register_funcs(_dll, globals())


# EOF
