# Integration with Twitter

from twython import Twython
from PIL import Image
from StringIO import StringIO

APP_KEY = 'ySpw09Es52O9gbsgJM68HBP2F'
APP_SECRET = 'lhZRj9R418U1W0OmA6NEJfhcHfQ2md4eRTBrjJvjjfxql9IRAC'

def get_auth():
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()

def update_image(shot):
    """ Upload the image in the file 'shot' to Twitter """
    # Requires Authentication as of Twitter API v1.1
    auth = get_auth()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # Tweet image: based on example at
    # https://twython.readthedocs.org/en/latest/usage/advanced_usage.html#updating-status-with-image
    photo = Image.open(shot)
    basewidth = 320
    wpercent = (basewidth/float(photo.size[0]))
    height = int((float(photo.size[1])*float(wpercent)))
    photo = photo.resize((basewidth, height), Image.ANTIALIAS)
    image_io = StringIO.StringIO()
    photo.save(image_io, format='JPEG')
    image_io.seek(0)

    twitter.update_status_with_media(media=photo, status='Bird spotted!')
