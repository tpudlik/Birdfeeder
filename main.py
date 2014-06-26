#!/usr/bin/python

# main module

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
from parameters import * # I don't like this approach, I'd like to validate
                         # the parameters.  How to do this better?

try:
    GPIO.setmode(GPIO.BCM)
    # Pin numbering scheme used, see
    # http://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering
    
    # Configure loggers  
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)
    file_log_handler = logging.FileHandler('birdfeeder.log')
    logger.addHandler(file_log_handler)
    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)
    
    formatter = logging.Formatter('%(asctime)s %(message)s')
    file_log_handler.setFormatter(formatter)
    stderr_log_handler.setFormatter(formatter)
    
    logger.info("Intializing detectors...")
    pir = PIR(PIR_PIN, DETECTOR_DELAY)
    ranger = Ranger(TRIG_PIN, ECHO_PIN, SETTLETIME, BACKGROUND, SAMPLES,
                    THRESHOLD)
    
    logger.info("Waiting for something to stir...")    
    while True:
        if pir.listen() and ranger.detect():
            image_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            image_name = image_name + '.jpeg'
            with picamera.PiCamera() as camera:
                camera.rotation = 180
                camera.capture(image_name)
                logger.info('Picture taken')
            if TWEET:
                twitter.update_image(image_name)
                time.sleep(PHOTO_DELAY)
except KeyboardInterrupt:
    logger.info('Keyboard interrupt: exiting.')
finally:
    GPIO.cleanup()
