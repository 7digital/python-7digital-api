import httplib
import oauth

# key and secret you got from 7digital when registering an application
CONSUMER_KEY = '7dnrt4z3uh'
CONSUMER_SECRET = 'gwwpdg2ht6vttfqp'

SERVER = 'api.7digital.com' 

REQUEST_TOKEN_URL = 'https://%s/1.2/oauth/requesttoken' % SERVER
ACCESS_TOKEN_URL = 'https://%s/1.2/oauth/accesstoken' % SERVER
AUTHORIZATION_URL = 'https://account.7digital.com/%s/oauth/authorise' % CONSUMER_KEY


# pass an oauth request to the server (using httplib.connection passed in as param)
# return the response as a string
def fetch_response(oauth_request, connection, debug=True):
	url= oauth_request.to_url()
	connection.request(oauth_request.http_method,url)
	response = connection.getresponse()
	s=response.read()
	
	return s

# main routine
def test_sevendigital():
    connection = httplib.HTTPSConnection(SERVER)
    consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
    
    token = request_token(consumer, signature_method, connection)
	
    authorized = authorize_request_token(token)
    
    access_token = request_access_token(consumer, signature_method, connection, token)
    return access_token
    
def request_token(consumer, signature_method, connection):
    print '\nOAUTH STEP 1'
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, http_url=REQUEST_TOKEN_URL, parameters={})
    oauth_request.sign_request(signature_method, consumer, None)
    resp=fetch_response(oauth_request, connection) 

    token=oauth.OAuthToken.from_string(resp)
    return token

def authorize_request_token(token):
    print '\nOAUTH STEP 2'
    auth_url="%s?oauth_token=%s" % (AUTHORIZATION_URL, token.key)

    # auth url to go to
    print 'Authorization URL:\n%s' % auth_url
    oauth_verifier = raw_input('Please go to the above URL and authorize the app. Hit return when you have been authorized: ')
    return True
    
def request_access_token(consumer, signature_method, connection, token):
    print '\nOAUTH STEP 3'
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=token, http_url=ACCESS_TOKEN_URL, parameters={})
    oauth_request.sign_request(signature_method, consumer, token)
    resp=fetch_response(oauth_request, connection) 

	token=oauth.OAuthToken.from_string(resp)
    return token

# app entry point
if __name__ == '__main__':
    test_sevendigital()
    print 'Done.'
