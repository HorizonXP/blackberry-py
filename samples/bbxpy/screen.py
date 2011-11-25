
from ctypes import POINTER, c_int, byref, cast, sizeof

import qnx.notification as qn

from .wrapped.bps import *
from .wrapped.screen import *


def showptr(p):
    return p.contents if p else 'NULL'


class Screen:
    _initialized = False

    def setup(self):
        usage = c_int(SCREEN_USAGE_NATIVE)

        self.screen_ctx = screen_context_t()
        self.screen_win = screen_window_t()
        self.screen_buf = screen_buffer_t()
        self.rect = (c_int * 4)()
        print('rect', list(self.rect))
        print('ctx', showptr(self.screen_ctx))
        print('win', showptr(self.screen_win))
        print('buf', showptr(self.screen_buf))

        # Setup the window
        rc = screen_create_context(byref(self.screen_ctx), 0)
        print('screen_create_context', rc)
        print('ctx', showptr(self.screen_ctx))

        screen_create_window(byref(self.screen_win), self.screen_ctx)
        print('win', showptr(self.screen_win))

        rc = screen_set_window_property_iv(self.screen_win, SCREEN_PROPERTY_USAGE, byref(usage))
        print('screen_set_window_property_iv', rc)

        rc = screen_create_window_buffers(self.screen_win, 1)
        print('screen_create_window_buffers', rc)

        rc = screen_get_window_property_pv(self.screen_win, SCREEN_PROPERTY_RENDER_BUFFERS,
            cast(byref(self.screen_buf), POINTER(c_void_p)))
        print('screen_get_window_property_pv', rc)
        print('buf', showptr(self.screen_buf))

        rc = screen_get_window_property_iv(self.screen_win, SCREEN_PROPERTY_BUFFER_SIZE,
            cast(byref(self.rect, 2 * sizeof(c_int)), POINTER(c_int)))
        print('screen_get_window_property_iv', rc)
        print('rect', list(self.rect))

        self.fill_screen(0xff0000ff)
        #~ # Signal bps library that navigator and screen events will be requested
        bps_initialize()
        screen_request_events(self.screen_ctx)
        navigator_request_events(0)

        self.domains = {
            audiodevice_get_domain(): 'audio',
            clock_get_domain(): 'clock',
            locale_get_domain(): 'locale',
            navigator_get_domain(): 'navigator',
            orientation_get_domain(): 'orientation',
            virtualkeyboard_get_domain(): 'virtualkeyboard',
            sensor_get_domain(): 'sensor',
            screen_get_domain(): 'screen',
            }
        print('domains', ', '.join('%s=%s' % (d,n) for d, n in sorted(self.domains.items())))
        self._initialized = True


    def fill_screen(self, colour):
        # Fill the screen buffer with blue
        attribs = (c_int * 3)(SCREEN_BLIT_COLOR, colour, SCREEN_BLIT_END)
        rc = screen_fill(self.screen_ctx, self.screen_buf, attribs)
        if rc:
            raise RuntimeError
        rc = screen_post_window(self.screen_win, self.screen_buf, 1, self.rect, 0)
        if rc:
            raise RuntimeError


    def cleanup(self):
        # Clean up
        screen_stop_events(self.screen_ctx)
        bps_shutdown()

        rc = screen_destroy_window(self.screen_win)
        print('screen_destroy_window', rc)

        rc = screen_destroy_context(self.screen_ctx)
        print('screen_destroy_context', rc)

        self._initialized = False


    # for now this stuff isn't integrated, but is called by scripts/event_test.py
    def poll(self):
        if self._initialized:
            # Handle user input
            self.handle_event()


    def handle_screen_event(self, event):
        screen_val = c_int()

        screen_event = screen_event_get_event(event)
        rc = screen_get_event_property_iv(screen_event, SCREEN_PROPERTY_TYPE, byref(screen_val))
        #~ print('screen_get_event_property_iv', rc)
        #~ print('screen event', screen_val.value)

        if screen_val.value == SCREEN_EVENT_MTOUCH_TOUCH:
            print('Touch event')
        elif screen_val.value == SCREEN_EVENT_MTOUCH_MOVE:
            print('Move event')
        elif screen_val.value == SCREEN_EVENT_MTOUCH_RELEASE:
            print('Release event')
        else:
            print('screen event, unknown', screen_val.value)


    def handle_navigator_event(self, event):
        event_code = bps_event_get_code(event)
        #~ print('nav event', event_code)
        if event_code == NAVIGATOR_SWIPE_DOWN:
            print('Swipe down event')
            self.notify1 = qn.SimpleNotification('Top-swipe!', timeout=3)

        elif event_code == NAVIGATOR_EXIT:
            print('Exit event')
            raise SystemExit('NAVIGATOR_EXIT')

        else:
            print('navigator event: unknown', event_code)


    def handle_event(self):
        event = POINTER(bps_event_t)()
        rc = bps_get_event(byref(event), -1)
        #~ print('bps_get_event', rc)
        assert rc == BPS_SUCCESS

        if event:
            domain = bps_event_get_domain(event.contents)
            if domain == navigator_get_domain():
                self.handle_navigator_event(event.contents)
            elif domain == screen_get_domain():
                self.handle_screen_event(event.contents)
            else:
                print('event:', self.domains.get(domain, domain))


# EOF
