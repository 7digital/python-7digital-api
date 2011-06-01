import httplib
import oauth

SERVER = 'api.7digital.com' 

REQUEST_TOKEN_URL = 'https://api.7digital.com/1.2/oauth/requesttoken'
ACCESS_TOKEN_URL = 'https://api.7digital.com/1.2/oauth/accesstoken'

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
    if debug:
        print 'requested URL: %s' % url
        print 'server response: %s' % s
    return s

# main routine
def test_sevendigital():
    # setup some variables that we'll use when we actually start doing things
    connection = httplib.HTTPSConnection(SERVER) # a connection we'll re-use a lot
    consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET) # just a place to store consumer key and secret
    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

# app entry point
if __name__ == '__main__':
    test_sevendigital()
    print 'Done.'
