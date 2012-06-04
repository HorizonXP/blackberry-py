# QNX's httplib2 points to a non-existent file.
# This is a hotfix to point to our own ca-certs.
import os
import httplib2
httplib2.CA_CERTS = os.path.join(os.path.dirname(__file__), 'ca-certificates.crt')
import oauth2
import urllib.parse as urlparse

from bottle import route, run, request, Bottle, ServerAdapter
import threading

from PySide.QtCore import *
from PySide.QtGui import *

class OAuthProvider(QObject):
    @Slot()
    def getAuthorization(self):
        self.consumer = oauth2.Consumer(self._getConsumerKey(), self._getConsumerSecret())
        self.client = oauth2.Client(self.consumer)

        # Step 1: Get a request token. This is a temporary token that is used for 
        # having the user authorize an access token and to sign the request to obtain 
        # said access token.
        resp, content = self.client.request(self._getRequestTokenURL(), "POST", 
                body=urlparse.urlencode({'oauth_callback':self._getCallbackURL()}))

        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        request_token = dict(urlparse.parse_qsl(content.decode()))
        self._oauthToken = request_token['oauth_token']
        self._oauthTokenSecret = request_token['oauth_token_secret']

        # Step 2: Redirect to the provider. Since this is a CLI script we do not 
        # redirect. In a web application you would redirect the user to the URL
        # below.
        x = "%s?oauth_token=%s" % (self._getAuthorizeURL(), self._getOAuthToken())
        QDesktopServices.openUrl(QUrl(x))
        
        # Step 3: Start a local server for service to callback to. That way, we
        # can receive the oauth_token and oauth_verifier.
        global query_vars
        query_vars = dict()
        self.callbackApp = Bottle()
        self.callbackApp.route(path='/%s' % self._getServiceName(),
                callback=OAuth_Route_Callback)
        self.server = CallbackServer(app=self.callbackApp, callback=self.receivedOAuthToken)
        self.server.start()

    def receivedOAuthToken(self, params):
        if 'oauth_token' in params and 'oauth_verifier' in params:
            # Grab the token and verifier
            self._oauthToken = params['oauth_token']
            self._oauthVerifier = params['oauth_verifier']
            # create a new token, and sign with verifier
            token = oauth2.Token(self._getOAuthToken(), self._getOAuthTokenSecret())
            token.set_verifier(self._getOAuthVerifier())
            # recreate the client with the new token
            self.client = oauth2.Client(self.consumer, token)

            # Get the new access tokens
            resp, content = self.client.request(self._getAccessTokenURL(), "POST")
            access_token = dict(urlparse.parse_qsl(content.decode()))
            # Replace our oauth token with the new ones 
            self._oauthToken = access_token['oauth_token']
            self._oauthTokenSecret = access_token['oauth_token_secret']
            # create a new token, and sign with verifier
            token = oauth2.Token(self._getOAuthToken(), self._getOAuthTokenSecret())
            # recreate the client with the new token
            self.client = oauth2.Client(self.consumer, token)
            self._authorized = True
            self.authorizationChanged.emit()

    @Slot()
    def logout(self):
        self._oauthToken = None
        self._oauthVerifier = None
        self._oauthTokenSecret = None
        self.consumer = None
        self.client = None
        self._authorized = False
        self.authorizationChanged.emit()


    @Signal
    def authorizationChanged(self): pass

    def _getAuthorized(self):
        return self._authorized

    @Signal
    def consumerKeyChanged(self): pass

    def _getConsumerKey(self):
        return self._consumerKey

    def _setConsumerKey(self, newKey):
        self._consumerKey = newKey

    @Signal
    def consumerSecretChanged(self): pass

    def _getConsumerSecret(self):
        return self._consumerSecret

    def _setConsumerSecret(self, newSecret):
        self._consumerSecret = newSecret

    @Signal
    def requestTokenURLChanged(self): pass

    def _getRequestTokenURL(self):
        return self._requestTokenURL

    def _setRequestTokenURL(self, newURL):
        self._requestTokenURL = newURL

    @Signal
    def accessTokenURLChanged(self): pass

    def _getAccessTokenURL(self):
        return self._accessTokenURL

    def _setAccessTokenURL(self, newURL):
        self._accessTokenURL = newURL

    @Signal
    def authorizeURLChanged(self): pass

    def _getAuthorizeURL(self):
        return self._authorizeURL

    def _setAuthorizeURL(self, newURL):
        self._authorizeURL = newURL

    @Signal
    def callbackURLChanged(self): pass

    def _getCallbackURL(self):
        return self._callbackURL

    @Signal
    def oauthTokenChanged(self): pass

    def _getOAuthToken(self):
        return self._oauthToken

    @Signal
    def oauthTokenSecretChanged(self): pass

    def _getOAuthTokenSecret(self):
        return self._oauthTokenSecret

    @Signal
    def oauthVerifierChanged(self): pass

    def _getOAuthVerifier(self):
        return self._oauthVerifier

    @Signal
    def serviceNameChanged(self): pass

    def _getServiceName(self):
        return self._serviceName

    def _setServiceName(self, newName):
        global OAuthServiceName
        OAuthServiceName = newName
        self._serviceName = newName
        self._callbackURL = "http://localhost:26100/%s" % newName

    _authorized = False
    _consumerKey = None
    _consumerSecret = None
    _requestTokenURL = None
    _accessTokenURL = None
    _callbackURL = None
    _authorizeURL = None
    _serviceName = None
    _oauthToken = None
    _oauthTokenSecret = None
    _oauthVerifier = None

    consumerKey = Property(str, _getConsumerKey, _setConsumerKey, notify=consumerKeyChanged)
    consumerSecret = Property(str, _getConsumerSecret, _setConsumerSecret, notify=consumerSecretChanged)
    requestTokenURL = Property(str, _getRequestTokenURL, _setRequestTokenURL, notify=requestTokenURLChanged)
    accessTokenURL = Property(str, _getAccessTokenURL, _setAccessTokenURL, notify=accessTokenURLChanged)
    authorizeURL = Property(str, _getAuthorizeURL, _setAuthorizeURL, notify=authorizeURLChanged)
    callbackURL = Property(str, _getCallbackURL, notify=callbackURLChanged)
    oauthToken = Property(str, _getOAuthToken, notify=oauthTokenChanged)
    oauthTokenSecret = Property(str, _getOAuthTokenSecret, notify=oauthTokenSecretChanged)
    oauthVerifier = Property(str, _getOAuthVerifier, notify=oauthVerifierChanged)
    serviceName = Property(str, _getServiceName, _setServiceName, notify=serviceNameChanged)
    authorized = Property(bool, _getAuthorized, notify=authorizationChanged)


class CallbackServer(threading.Thread):
    def __init__(self, app=None, callback=None):
        super(CallbackServer, self).__init__()
        self.event = threading.Event()
        self.callback = callback
        self.app = app
    def run(self):
        run(app=self.app, server=CallbackRefServer, host='localhost', port=26100)
        self.callback and self.callback(query_vars)

class CallbackRefServer(ServerAdapter):
    def run(self, handler): # pragma: no cover
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.handle_request()

def OAuth_Route_Callback():
    if 'denied' in request.GET:
        query_vars['denied'] = request.GET['denied']
        return "DENIED!"
    elif 'oauth_token' in request.GET and 'oauth_verifier' in request.GET:
        query_vars['oauth_verifier'] = request.GET['oauth_verifier']
        query_vars['oauth_token'] = request.GET['oauth_token']
        return "You're in!"
    else:
        return "You shouldn't be here!"
