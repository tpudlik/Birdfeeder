# Integration with Twitter

import logging
from twython import Twython, TwythonError
from access_tokens import T_APP_KEY, T_APP_SECRET, T_OAUTH_TOKEN, T_OAUTH_TOKEN_SECRET

def update_image(shot, status='Bird spotted!'):
    """ Upload the image in the file 'shot' to Twitter account. """
    # Requires Authentication as of Twitter API v1.1
    logger = logging.getLogger('main.twitter')
    twitter = Twython(T_APP_KEY, T_APP_SECRET,
                      T_OAUTH_TOKEN, T_OAUTH_TOKEN_SECRET)
    photo = open(shot, 'rb')
    try:
        twitter.update_status_with_media(media=photo, status=status)
    except TwythonError:
        logger.error('Photo tweeting failed')
    else:
        logger.info('Photo tweeted')
