#!/usr/bin/python

""" 
Wait for the IRon curtain to be tripped, then take a picture.  Upload the picture
to Twitter and Dropbox.
"""

import os, datetime, logging
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
with Tripwire(settletime=SETTLETIME,
              detector_delay=DETECTOR_DELAY,
              sensor_pin=SENSOR_PIN) as t:
    while True:
        if t.listen():
            images = []
            for img in range(PHOTO_BURST):
                image_name = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                image_name = image_name + '.jpeg'
                with picamera.PiCamera() as camera:
                    if PHOTO_ROTATE:
                        camera.rotation = PHOTO_ROTATE
                    camera.resolution = (2592, 1944) # Full sensor size
                    if TWEET and not DBOX:
                        # Crop the image to the 2:1 aspect Twitter likes
                        camera.zoom(0, 1.0/3, 1, 1)
                        camera.capture(image_name,
                                       resize=(2592, int(2.0/3*1944)))
                    else:
                        camera.capture(image_name)
                    logger.info('Picture taken')
                images.append(image_name)
            for image_name in images:
                if DBOX:
                    dbox.upload(image_name)
                if TWEET:
                    twitter.update_image(image_name)
                if DBOX or TWEET:
                    # The image was uploaded to external server, can be
                    # safely removed.
                    os.remove(image_name)
