'''Demonstrate geolocation interface.

Note that in the 2.0.0.3894 implementation qnx.geolocation, there's
a bug involving strings versus bytes and the PpsObject values,
requiring some form of patching to work around.  You could patch
Geolocation._build_request() to fix things in the one direction,
or fix the response back to Geolocation._get_update() for the other
direction. For fairly arbitrary reasons I chose the latter approach.'''

import time
from qnx.geolocation import Geolocation
import qnx.notification as qn


class GeoTracer:
    def __init__(self):
        self.geo = Geolocation(self.on_location, self.on_status)
        self.updating = False


    def _fix_read(self):
        '''Intercept data read back from PpsFile to tweak the result value
        so it's the expected string instead of bytes.'''
        resp = self._f_read()
        try:
            value = resp[Geolocation._KEY_RES]
            resp[Geolocation._KEY_RES] = value.decode()
        except AttributeError:
            pass

        #~ print('data', resp)
        return resp


    def run(self):
        self.geo.open_connection()

        # hotpatch the Geolocation's PpsFile object to fix the data read back
        self._f_read = self.geo.f.read
        self.geo.f.read = self._fix_read

        try:
            self.geo.start_location_updates(1.0)

            start = time.time()
            while time.time() - start < 60:
                time.sleep(5)
                if not self.updating:
                    print('waiting', self.geo.status_of_location_updates())

            self.geo.cancel_location_updates()
        finally:
            self.geo.f.read = self._f_read # undo hotpatching
            self.geo.close_connection()


    def on_location(self, latitude, longitude, accuracy, altitude, altitude_accuracy, heading, speed, *args):
        if not self.updating:
            self.notify = qn.SimpleNotification('Geotrace: location found!',
                showTimeFlag=True,
            )

        self.updating = True
        print('(%.6f, %.6f) acc=%5.1fm elev=%4.0fm heading=%3.0f speed=%4.1fm/s' % (latitude, longitude, accuracy, altitude, heading, speed))


    def on_status(self, status, *args):
        print('status', status)



def run():
    geo = GeoTracer()
    geo.run()
