import httplib
import oauth
    
class Oauth7digital(object):
    key = None

    SERVER = 'api.7digital.com'
    REQUEST_TOKEN_URL = 'https://%s/1.2/oauth/requesttoken' % SERVER
    ACCESS_TOKEN_URL = 'https://%s/1.2/oauth/accesstoken' % SERVER

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def request_token(self):
        print '\nOAUTH STEP 1'
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.__consumer(), http_url = self.REQUEST_TOKEN_URL, parameters={})
        print '\nMESSAGE:: %s' %oauth_request
        oauth_request.sign_request(self.__signature_method(), self.__consumer(), None)
        resp = self.__fetch_response(oauth_request, self.__connection()) 

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
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.__consumer(), token=token, http_url = self.ACCESS_TOKEN_URL, parameters={})
        oauth_request.sign_request(self.__signature_method(), self.__consumer(), token)
        resp = self.__fetch_response(oauth_request, self.__connection()) 

        token = oauth.OAuthToken.from_string(resp)
        return token
      
    def __consumer(self):
        return oauth.OAuthConsumer(self.key, self.secret)
    
    def __signature_method(self):
        return oauth.OAuthSignatureMethod_HMAC_SHA1()
        
    def __connection(self):
        return httplib.HTTPSConnection(self.SERVER)
        
    def __fetch_response(self, oauth_request, connection):
	    url = oauth_request.to_url()
	    connection.request(oauth_request.http_method, url)
	    response = connection.getresponse()
	    result = response.read()
	
	    return result

