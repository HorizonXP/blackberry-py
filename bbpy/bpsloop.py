'''Thread providing event handling loop for libbps events.'''

import sys
import threading

from ctypes import POINTER, c_int, byref, cast, sizeof

from .wrapped.bps import *


def showptr(p):
    return p.contents if p else 'NULL'


NAV_EVENT_NAMES = {
    NAVIGATOR_INVOKE              : 'invoke',
    NAVIGATOR_EXIT                : 'exit',
    NAVIGATOR_WINDOW_STATE        : 'window_state',
    NAVIGATOR_LOW_MEMORY          : 'low_memory',
    NAVIGATOR_SWIPE_DOWN          : 'swipe_down',
    NAVIGATOR_SWIPE_START         : 'swipe_start',
    NAVIGATOR_ORIENTATION_CHECK   : 'orientation_check',
    NAVIGATOR_ORIENTATION         : 'orientation',
    NAVIGATOR_BACK                : 'back',
    NAVIGATOR_WINDOW_ACTIVE       : 'window_active',
    NAVIGATOR_WINDOW_INACTIVE     : 'window_inactive',
    NAVIGATOR_ORIENTATION_DONE    : 'orientation_done',
    NAVIGATOR_ORIENTATION_RESULT  : 'orientation_result',
    NAVIGATOR_WINDOW_LOCK         : 'window_lock',
    NAVIGATOR_WINDOW_UNLOCK       : 'window_unlock',
    }


WINDOW_STATE_NAMES = {
    NAVIGATOR_WINDOW_FULLSCREEN   : 'fullscreen',
    NAVIGATOR_WINDOW_THUMBNAIL    : 'thumbnail',
    NAVIGATOR_WINDOW_INVISIBLE    : 'hidden',
    }


class BpsThread(threading.Thread):
    _initialized = False

    def __init__(self, signal=None):
        super(BpsThread, self).__init__()
        self.daemon = True

        self._signal = signal
        self.missed = []
        self.windowGroup = ''

        bps_initialize()
        # bps_set_verbosity(2)
        # print('bps_version', bps_get_version(), file=sys.stderr)
        self.missed.append('bps_version {}'.format(bps_get_version()))

        self._domain = bps_register_domain()

        self._wake_event = POINTER(bps_event_t)()
        rc = bps_event_create(byref(self._wake_event), self._domain, 0, None, bps_event_completion_func())

        self._channel = bps_channel_get_active()


    def _get_signal(self):
        return self._signal
    def _set_signal(self, signal):
        self._signal = signal
        if self._wake_event:
            self.missed.append('waking up on {}'.format(self._channel))
            bps_channel_push_event(self._channel, self._wake_event)

    signal = property(_get_signal, _set_signal)


    def notify(self, msg, args):
        try:
            text = msg.format(args)
        except Exception:
            text = '(misformed msg)'
        # print('!!--notify: ' + text, file=sys.stderr)
        if self._signal:
            if self.missed:
                for t in self.missed:
                    self._signal.emit(t)
                del self.missed[:]
            self._signal.emit(text)
        else:
            self.missed.append(text)


    def setup(self):
        # screen_request_events(self.screen_ctx)
        navigator_request_events(0)
        # navigator_request_swipe_start()

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
        self.notify('domains {}',
            ', '.join('%s=%s' % (d,n) for d, n in sorted(self.domains.items())))

        self._initialized = True


    def cleanup(self):
        # Clean up
        # screen_stop_events(self.screen_ctx)
        bps_shutdown()

        self._initialized = False


    def handle_navigator_event(self, event):
        event_code = bps_event_get_code(event)

        self._ecode = event_code

        # print('---> {} {!r}'.format(type(event_code), event_code), file=sys.stderr)
        self.notify('nav event: {}',
            NAV_EVENT_NAMES.get(event_code, event_code))

        if event_code == NAVIGATOR_INVOKE:
            data = navigator_event_get_data(event)
            self.notify('  data: {}', data.decode('ascii'))

        elif event_code == NAVIGATOR_WINDOW_ACTIVE:
            groupid = navigator_event_get_groupid(event)
            self.notify('  groupid: {}', groupid.decode('ascii'))
            # store this as it's the first event we'll see with this info
            if not self.windowGroup:
                self.windowGroup = groupid.decode('ascii')
            # self._initialized = False

        elif event_code == NAVIGATOR_WINDOW_INACTIVE:
            groupid = navigator_event_get_groupid(event)
            self.notify('  groupid: {}', groupid.decode('ascii'))

        elif event_code == NAVIGATOR_WINDOW_STATE:
            window_state = navigator_event_get_window_state(event)
            self.notify('  window state: {}',
                WINDOW_STATE_NAMES.get(window_state, window_state))
            try:
                groupid = navigator_event_get_groupid(event)
                self.notify('  groupid: {}', groupid.decode('ascii'))
            except Exception as ex:
                self.notify('exception {!r}', ex)

        # if asked if we'll change orientations, respond
        elif event_code == NAVIGATOR_ORIENTATION_CHECK:
            eventid = navigator_event_get_id(event)
            self.notify('  eventid: {}', eventid.decode('ascii'))
            angle = navigator_event_get_orientation_angle(event)
            self.notify('  angle: {}', angle)
            navigator_orientation_check_response(event, True)

        elif event_code == NAVIGATOR_ORIENTATION_DONE:
            angle = navigator_event_get_orientation_angle(event)
            self.notify('  angle: {}', angle)
            navigator_done_orientation(event)

        elif event_code == NAVIGATOR_ORIENTATION_RESULT:
            angle = navigator_event_get_orientation_angle(event)
            self.notify('  angle: {}', angle)

        elif event_code == NAVIGATOR_EXIT:
            self._initialized = False
            error = navigator_event_get_err(event)
            if error:
                self.notify('  error: {}', errtext.decode('ascii'))


    def handle_event(self):
        event = POINTER(bps_event_t)()

        self._event = event

        rc = bps_get_event(byref(event), -1)
        # self.notify('bps_get_event {}', rc)
        assert rc == BPS_SUCCESS

        if event:
            domain = bps_event_get_domain(event.contents)
            # print('---> domain {!r}'.format(domain), file=sys.stderr)
            if domain == navigator_get_domain():
                self.handle_navigator_event(event.contents)
            else:
                self.notify('event domain: {}', self.domains.get(domain, domain))


    def run(self):
        '''Event handling loop run here.'''
        self.setup()

        try:
            while self._initialized:
                # Handle user input
                self.handle_event()

        finally:
            self.cleanup()


# EOF
