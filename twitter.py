# Integration with Twitter

from twython import Twython

APP_KEY = 'ySpw09Es52O9gbsgJM68HBP2F'
APP_SECRET = 'lhZRj9R418U1W0OmA6NEJfhcHfQ2md4eRTBrjJvjjfxql9IRAC'
OAUTH_TOKEN = '2429040776-0rkZJGKOpG5jdLe9UG1oxpRCx8x3IcWUadR8m8e'
OAUTH_TOKEN_SECRET = 'yEfYZUd9M9JWtWHlx4XbDXdUmClH1sGCMpwsBNXtcpUwY'

def get_auth():
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()

def update_image(shot, status='Bird spotted!'):
    """ Upload the image in the file 'shot' to Twitter account """
    # Requires Authentication as of Twitter API v1.1
    # The lines below are apparently unnecessary---we already know the
    # OAUTH_TOKEN and OAUTH_TOKEN_SECRET.
    #auth = get_auth()
    #OAUTH_TOKEN = auth['oauth_token']
    #OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    photo = open(shot, 'rb')
    twitter.update_status_with_media(media=photo, status=status)
