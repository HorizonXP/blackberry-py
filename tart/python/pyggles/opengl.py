
import sys
import os
import threading
import queue
import traceback
from ctypes import (byref, c_int, cast, c_void_p, c_float, CDLL)

from bb import gles
from bb.egl import EGLint, EGL_BAD_NATIVE_WINDOW
from tart import window, dynload
from . import egl

# support library
_ogl = dynload('_opengl')



class OglContext:
    def __init__(self, egl):
        self._egl = egl
        self.sw = self.sh = None
        self.get_surface_size()


    #-----------------------------------------------
    #
    def get_surface_size(self):
        sw, sh = self._egl.get_surface_size()

        # FIXME: this is an ugly wart... need to study the connections
        # between libscreen and EGL better so we can figure out how
        # best to handle this, since it will change if we let the onscreen
        # window change size.

        changed = False

        # update sizes of "surface" (same as libscreen source viewport?)
        # so the fonts will be scaled and positioned properly
        if sw != self.sw:
            swidth = egl.EGLint.in_dll(_ogl, 'surface_width')
            swidth.value = sw
            self.sw = sw
            changed = True

        if sh != self.sh:
            sheight = egl.EGLint.in_dll(_ogl, 'surface_height')
            sheight.value = sh
            self.sh = sh
            changed = True

        if changed:
            print('NEW surface size:', sw, sh)

        return sw, sh



class OglThread(threading.Thread):
    #-----------------------------------------------
    #
    def __init__(self):
        super().__init__(name='ogl')
        self.daemon = True
        self.queue = queue.Queue()

        self._window = self._egl = self._ogl = None
        self._visible = True

        self.start()


    #-----------------------------------------------
    #
    def send(self, args):
        self.queue.put(args)


    #-----------------------------------------------
    #
    def register(self, window):
        self.queue.put((self._register, (window,)))


    #-----------------------------------------------
    #
    def _register(self, window):
        self._egl = egl.EglContext()
        self._egl.initialize(window.native_window)
        self._ogl = OglContext(self._egl)

        self._window = window
        self._window.setup(self._ogl)


    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value


    #-----------------------------------------------
    #
    def setup(self):
        print('OGL: set up')


    #-----------------------------------------------
    #
    def cleanup(self):
        print('OGL: cleaned up')


    #-----------------------------------------------
    #
    def run(self):
        print('OGL: running')

        try:
            self.setup()

            while True:
                try:
                    self.process_messages()

                    self.do_render()

                except SystemExit:
                    raise

                except:
                    traceback.print_exception(*sys.exc_info())

        finally:
            self.cleanup()


    #-----------------------------------------------
    #
    def process_messages(self):
        while True:
            timeout = 1.0
            try:
                # print('get msg, timeout', timeout)
                msg = self.queue.get(timeout=timeout)
            except queue.Empty:
                # self._window.redraw = True
                break

            try:
                handler, pargs, kwargs = msg
            except ValueError:
                kwargs = {}
                try:
                    handler, pargs = msg
                except ValueError:
                    pargs = ()
                    handler, = msg

            print('OGL: call {} {} {}'.format(handler, pargs, kwargs))
            handler(*pargs, **kwargs)


    _draw_count = 0
    _render_count = 0
    PACE = 10

    #-----------------------------------------------
    #
    def do_render(self):
        if self._window and self._visible:
            # hack: triggers update and print and stuff... TODO: remove this
            self._ogl.get_surface_size()

            if self._window.redraw:
                if self._draw_count % self.PACE == 0:
                    print('#{}: draw'.format(self._draw_count))
                self._draw_count += 1

                self._window.redraw = False
                try:
                    self._window.draw(self._ogl)
                    self._window.rerender = True
                except:
                    self._window.rerender = False
                    raise

            if self._window.rerender:
                # if self._render_count % self.PACE == 0:
                #     print('#{}: render'.format(self._render_count))
                self._render_count += 1

                self._window.rerender = False
                self._window.render(self._ogl)

                try:
                    self._egl.swap()
                except egl.EglError as ex:
                    if ex.error == egl.EGL_BAD_NATIVE_WINDOW:
                        self._egl.destroy_surface()
                        self._egl.create_surface(self._window.native_window)

                        self._window.redraw = True
                    else:
                        raise


class OglWindow:
    '''Class representing a window to be rendered in an OglThread.'''

    #-----------------------------------------------
    #
    def __init__(self, group, id, size):
        self._window = window.NativeWindow(group, id, size)
        print('window', self._window)

        disp = self._window.display
        print('disp', disp)

        dpi = disp.get_dpi()
        print('dpi', dpi)

        self._size = (0, 0)

        self.redraw = True
        self.rerender = True

        self._thread = OglThread()
        self._thread.register(self)


    @property
    def native_window(self):
        return self._window._win


    @property
    def size(self):
        self._size

    @size.setter
    def size(self, value):
        newsize = (int(value[0]), int(value[1]))
        if newsize != self._size:
            self._thread.send((self._set_size, value))
            self._size = newsize    # here or in thread?
        # else:
        #     print('size unchanged, ignoring')


    # @in_render
    def _set_size(self, w, h):
        print('OglWindow.size = ({},{})'.format(w, h))
        self._window.buffer_size = (w, h)
        self.redraw = True


    @property
    def window_state(self):
        return self._window_state
    @window_state.setter
    def window_state(self, value):
        self._window_state = value
        self._thread.visible = value == 'fullscreen'


    #-----------------------------------------------
    #
    @property
    def context(self):
        return self._context


    #-----------------------------------------------
    #
    @staticmethod
    def make_vector(data, type=gles.GLfloat):
        '''Utility method to turn a sequence of data into a ctypes array
        of the given type, defaulting to GLfloat.'''
        vector = (type * len(data))(*data)
        return vector


    #-----------------------------------------------
    #
    @staticmethod
    def make_strip_vector(points):
        strip = []
        points = iter(points)
        for p in zip(points, points):
            strip.extend(p)
            strip.append(p[0])
            strip.append(0)

        return OglWindow.make_vector(strip)


    #-----------------------------------------------
    # To be overridden in subclass.
    #
    def setup(self, ctx):
        pass


    #-----------------------------------------------
    # To be overridden in subclass.
    #
    def draw(self, ctx):
        pass


    #-----------------------------------------------
    # To be overridden in subclass.
    #
    def render(self, ctx):
        from random import random
        gles.glClearColor(random(), random(), random(), 1.0)
        gles.glClear(gles.GL_COLOR_BUFFER_BIT | gles.GL_DEPTH_BUFFER_BIT)


# EOF
