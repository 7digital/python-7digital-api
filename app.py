import pickle # for storing access token to file
from lib.oauth7digital import Oauth7digital
# key and secret you got from 7digital when registering an application


TOKEN_FILE = './access_token.pkl'

def test_sevendigital():
    try:
        pkl_file = open(TOKEN_FILE, 'rb')
        access_token = pickle.load(pkl_file)
        pkl_file.close()
    except:
        access_token = None
    if access_token:
        print 'You have an access token: %s' % str(access_token.key)
    else:
        auth = Oauth7digital(CONSUMER_KEY, CONSUMER_SECRET)

        token = auth.request_token()
	
        authorized = auth.authorize_request_token(token)
        
        access_token = auth.request_access_token(token)
        print 'MESSAGE:: access token: %s' % access_token
        
        pkl_file=open(TOKEN_FILE, 'wb')
        pickle.dump(access_token, pkl_file)
        pkl_file.close()

# app entry point
if __name__ == '__main__':
    test_sevendigital()
    print 'Done.'
