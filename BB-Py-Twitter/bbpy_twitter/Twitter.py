from .OAuthProvider import OAuthProvider
from PySide.QtCore import *
import urllib.parse as urlparse
import json
import http.client

class Twitter(OAuthProvider):
    def __init__(self):
        super(Twitter, self).__init__()
        self._setRequestTokenURL('https://api.twitter.com/oauth/request_token')
        self._setAuthorizeURL('https://api.twitter.com/oauth/authorize')
        self._setAccessTokenURL('https://api.twitter.com/oauth/access_token')
        self._setServiceName('twitter')
        self.authorizationChanged.connect(self.getUserProfileData)

    @Slot()
    def getUserProfileData(self):
        if self.authorized:
            reqURL = 'https://api.twitter.com/1/account/verify_credentials.json'
            resp, content = self.client.request(reqURL, 
                    headers={'Authorization': 'OAuth'})
            if resp['status'] != '200':
                raise Exception("Invalid response %s." % resp['status'])
            retVal = json.loads(content.decode())
            self._screenName = retVal['screen_name']
            self._realName = retVal['name']
            self._timeZone = retVal['time_zone']
            self._description = retVal['description']
            self._id = retVal['id_str']
            self._location = retVal['location']
            try:
                params = urlparse.urlencode({'screen_name': self._screenName, 
                            'size': 'original'})
                reqURL = '/1/users/profile_image?%s' % params
                conn = http.client.HTTPSConnection('api.twitter.com')
                conn.request('GET', reqURL)
                r1 = conn.getresponse()
                if (r1.status == 302):
                    self._profileImage = r1.getheader('Location')
                else:
                    raise
            except Exception as e:
                print(e)
                self._profileImage = retVal['profile_image_url']
                
        else:
            self._screenName = None
            self._realName = None
            self._timeZone = None
            self._description = None
            self._id = None
            self._location = None
            self._profileImage = None

        self.screenNameChanged.emit()
        self.realNameChanged.emit()
        self.timeZoneChanged.emit()
        self.descriptionChanged.emit()
        self.idChanged.emit()
        self.locationChanged.emit()
        self.profileImageChanged.emit()

    @Signal
    def screenNameChanged(self): pass
    def _getScreenName(self):
        return self._screenName
    _screenName = None
    screenName = Property(str, _getScreenName, notify=screenNameChanged)

    @Signal
    def realNameChanged(self): pass
    def _getRealName(self):
        return self._realName
    _realName = None
    realName = Property(str, _getRealName, notify=realNameChanged)

    @Signal
    def timeZoneChanged(self): pass
    def _getTimeZone(self):
        return self._timeZone
    _timeZone = None
    timeZone = Property(str, _getTimeZone, notify=timeZoneChanged)

    @Signal
    def descriptionChanged(self): pass
    def _getDescription(self):
        return self._description
    _description = None
    description = Property(str, _getDescription, notify=descriptionChanged)

    @Signal
    def idChanged(self): pass
    def _getID(self):
        return self._id
    _id = None
    id = Property(str, _getID, notify=idChanged)

    @Signal
    def locationChanged(self): pass
    def _getLocation(self):
        return self._location
    _location = None
    location = Property(str, _getLocation, notify=locationChanged)

    @Signal
    def profileImageChanged(self): pass
    def _getProfileImage(self):
        return self._profileImage
    _profileImage = None
    profileImage = Property(str, _getProfileImage, notify=profileImageChanged)

