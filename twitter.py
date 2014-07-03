# Integration with Twitter

import logging
from twython import Twython, TwythonError
from access_tokes import D_APP_KEY, D_APP_SECRET, D_OAUTH_TOKEN, D_OAUTH_SECRET

def get_auth():
    """ Get OAUTH tokens.  (This function isn't actually used.)"""
    twitter = Twython(D_APP_KEY, D_APP_SECRET)
    auth = twitter.get_authentication_tokens()
    return auth

def update_image(shot, status='Bird spotted!'):
    """ Upload the image in the file 'shot' to Twitter account. """
    # Requires Authentication as of Twitter API v1.1
    logger = logging.getLogger('main.twitter')
    twitter = Twython(D_APP_KEY, D_APP_SECRET,
                      D_OAUTH_TOKEN, D_OAUTH_TOKEN_SECRET)
    photo = open(shot, 'rb')
    try:
        twitter.update_status_with_media(media=photo, status=status)
        logger.info('Photo tweeted')
    except TwythonError:
        logger.error('Photo tweeting failed')

