#!/usr/bin/python

""" 
Wait for the IRon curtain to be tripped, then take a picture.  Upload the picture
to Twitter and Dropbox.
"""

import time
import datetime
import logging
import picamera
from parameters import * # I don't like this approach, I'd like to validate
                         # the parameters.  How to do this better?
from iron_curtain import Tripwire
if TWEET:
    import twitter
if DBOX:
    import dbox

# Configure loggers
# ============================================================================
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')

file_log_handler = logging.FileHandler('birdfeeder.log')
file_log_handler.setFormatter(formatter)
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
stderr_log_handler.setFormatter(formatter)
logger.addHandler(stderr_log_handler)
# ============================================================================

logger.info('Initializing detectors...')
with Tripwire(settletime=SETTLETIME, detector_delay=DETECTOR_DELAY) as t:
    while True:
        previous_tweet_time = time.time()
        if t.listen():
            images = []
            for img in range(PHOTO_BURST):
                image_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                image_name = image_name + '.jpeg'
                with picamera.PiCamera() as camera:
                    camera.rotation = 180
                    camera.resolution = (2592, 1944) # Full sensor size
                    camera.capture(image_name)
                    logger.info('Picture taken')
                images.append(image_name)
            for image_name in images:
                if DBOX:
                    dbox.upload(image_name)
                if TWEET and ranger_confirmed and time.time() - previous_tweet_time > PHOTO_DELAY:
                    twitter.update_image(image_name)
                    previous_tweet_time = time.time()
