import httplib
import oauth
from lockerEndpoint import Locker
    
class Oauth7digital(object):
    key = None

    SERVER = 'api.7digital.com'
    REQUEST_TOKEN_URL = 'https://%s/1.2/oauth/requesttoken' % SERVER
    ACCESS_TOKEN_URL = 'https://%s/1.2/oauth/accesstoken' % SERVER
    LOCKER_ENDPOINT_URL = 'http://%s/1.2/user/locker' %SERVER

    def __init__(self, key, secret, access_token = None):
        self.key = key
        self.secret = secret
        self.access_token = access_token

    def request_token(self):
        print '\nOAUTH STEP 1'
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.__consumer(), http_url = self.REQUEST_TOKEN_URL, parameters={})
        print '\nMESSAGE:: %s' %oauth_request
        oauth_request.sign_request(self.__signature_method(), self.__consumer(), None)
        resp = self.__fetch_response(oauth_request, self.__secure_connection()) 

        token = oauth.OAuthToken.from_string(resp)
        return token

    def authorize_request_token(self, token):
        AUTHORIZATION_URL = 'https://account.7digital.com/%s/oauth/authorise' % self.key
        print '\nOAUTH STEP 2'
        auth_url="%s?oauth_token=%s" % (AUTHORIZATION_URL, token.key)

        # auth url to go to
        print 'Authorization URL:\n%s' % auth_url
        oauth_verifier = raw_input('Please go to the above URL and authorize the app. Hit return when you have been authorized: ')
        return True
    
    def request_access_token(self, token):
        print '\nOAUTH STEP 3'
        oauth_request = self.__sign_oauth_request(token, self.ACCESS_TOKEN_URL)
        resp = self.__fetch_response(oauth_request, self.__secure_connection()) 

        token = oauth.OAuthToken.from_string(resp)
        return token
    
    def get_user_locker(self):
        resp = self.__get_locker()
        return Locker(resp).get_content()
    
    def get_artist_from_user_locker(self):
        resp = self.__get_locker()
        return Locker(resp).get_artists()
    
    def get_releases_from_user_locker(self):
        resp = self.__get_locker()
        return Locker(resp).get_releases()
    
    def get_tracks_from_user_locker(self):
        resp = self.__get_locker()
        return Locker(resp).get_tracks()
    
    def get_locker(self):
        resp = self.__get_locker()
        return Locker(resp).get_contents()
    
    def __get_locker(self):
        oauth_request = self.__sign_oauth_request(self.access_token, self.LOCKER_ENDPOINT_URL)
        resp = self.__fetch_response(oauth_request, self.__connection())
        return resp
    
    def __sign_oauth_request(self, token, url_end_point):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.__consumer(), token=token, http_url = url_end_point, parameters={})
        
        oauth_request.sign_request(self.__signature_method(), self.__consumer(), token)
        return oauth_request
      
    def __consumer(self):
        return oauth.OAuthConsumer(self.key, self.secret)
    
    def __signature_method(self):
        return oauth.OAuthSignatureMethod_HMAC_SHA1()
        
    def __secure_connection(self):
        return httplib.HTTPSConnection(self.SERVER)
    
    def __connection(self):
        return httplib.HTTPConnection(self.SERVER)
        
    def __fetch_response(self, oauth_request, connection):
	    url = oauth_request.to_url()
	    connection.request(oauth_request.http_method, url)
	    response = connection.getresponse()
	    result = response.read()
	
	    return result

