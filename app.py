import pickle
from lib.oauth7digital import Oauth7digital


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
        
        pkl_file=open(TOKEN_FILE, 'wb')
        pickle.dump(access_token, pkl_file)
        pkl_file.close()
        
    return access_token
        
def test_locker():
    access_token = test_sevendigital()
    
    sevendigital = Oauth7digital(CONSUMER_KEY, CONSUMER_SECRET, access_token)
    result = sevendigital.get_user_locker()
    print result.get_release()
    return result.get_release()

# app entry point
if __name__ == '__main__':
    test_locker()
    print 'Done.'
    
    
    
