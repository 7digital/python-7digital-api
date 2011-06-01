import httplib
import oauth

SERVER = 'api.7digital.com' 

REQUEST_TOKEN_URL = 'https://'+SERVER+'/1.2/oauth/requesttoken'
ACCESS_TOKEN_URL = 'https://'+SERVER+'/1.2/oauth/accesstoken'

# key and secret you got from 7digital when registering an application
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

# pass an oauth request to the server (using httplib.connection passed in as param)
# return the response as a string
def fetch_response(oauth_request, connection, debug=True):
	url= oauth_request.to_url()
	connection.request(oauth_request.http_method,url)
	response = connection.getresponse()
	s=response.read()
    #if debug:
	print 'requested URL: %s' % url
	print 'server response: %s' % s
	return s

# main routine
def test_sevendigital():
	# setup some variables that we'll use when we actually start doing things
	connection = httplib.HTTPSConnection(SERVER) # a connection we'll re-use a lot
	consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET) # just a place to store consumer key and secret
	signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

	oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, http_url=REQUEST_TOKEN_URL, parameters={}) # create an oauth request
	oauth_request.sign_request(signature_method, consumer, None) # the request knows how to generate a signature
	resp=fetch_response(oauth_request, connection) # use our fetch_response method to send the request to Fire Eagle
	print '\nFire Eagle response was: %s' % resp
	token=oauth.OAuthToken.from_string(resp) # parse the response into an OAuthToken object
	print '\nkey: %s' % str(token.key)
	print 'secret: %s' % str(token.secret)
	
	
	oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=token, http_url=ACCESS_TOKEN_URL, parameters={})
	oauth_request.sign_request(signature_method, consumer, token)
	resp=fetch_response(oauth_request, connection) # use our fetch_response method to send the request to Fire Eagle
	print '\nFire Eagle response was: %s' % resp
	# now the token we get back is an access token
	token=oauth.OAuthToken.from_string(resp) # parse the response into an OAuthToken object
	print '\nkey: %s' % str(token.key)
	print 'secret: %s' % str(token.secret)

# app entry point
if __name__ == '__main__':
    test_sevendigital()
    print 'Done.'
