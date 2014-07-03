#!/usr/bin/python

""" 
Check signal from IR motion sensor every second, use the sonic ranger to
double-check if signal is detected, and take a picture if there seems to be
a bird out there.  Tweet the picture afterwards!
"""

import time
import datetime
import logging
import twitter
import picamera
import RPi.GPIO as GPIO
from passive_IR import PIR
from usonic import Ranger
import dbox
from parameters import * # I don't like this approach, I'd like to validate
                         # the parameters.  How to do this better?

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

try:
    GPIO.setmode(GPIO.BCM)
    # Pin numbering scheme used, see
    # http://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering
    
    logger.info("Initializing detectors...")
    pir = PIR(PIR_PIN, DETECTOR_DELAY)
    ranger = Ranger(TRIG_PIN, ECHO_PIN, SETTLETIME, BACKGROUND, SAMPLES,
                    THRESHOLD, DETECT_SAMPLES)
    
    logger.info("Waiting for something to stir...")
    previous_tweet_time = time.time()
    while True:
        if pir.listen():
            ranger_confirmed = ranger.detect()
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
except KeyboardInterrupt:
    logger.info('Keyboard interrupt: exiting.')
finally:
    GPIO.cleanup()
