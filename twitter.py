# Integration with Twitter

import logging, time
from twython import Twython, TwythonError
from access_tokens import T_APP_KEY, T_APP_SECRET, T_OAUTH_TOKEN, T_OAUTH_TOKEN_SECRET
from parameters import PHOTO_DELAY

previous_tweet_time = {'t': 0}
def update_image(shot, status='Bird spotted!'):
    """ Upload the image in the file 'shot' to Twitter account. """
    # Requires Authentication as of Twitter API v1.1
    if time.time() - previous_tweet_time['t'] > PHOTO_DELAY:
        logger = logging.getLogger('main.twitter')
        twitter = Twython(T_APP_KEY, T_APP_SECRET,
                          T_OAUTH_TOKEN, T_OAUTH_TOKEN_SECRET)
        with open(shot, 'rb') as photo:
            try:
                ids = twitter.upload_media(media=photo)
                twitter.update_status(media_ids=[ids['media_id']],
                                      status=status)
            except TwythonError:
                logger.exception('Photo tweeting failed')
            else:
                previous_tweet_time['t'] = time.time()
                logger.info('Photo tweeted')
