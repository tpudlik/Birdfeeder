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
from passive_IR import PIR
from usonic import Ranger
from parameters import * # I don't like this approach, I'd like to validate
                         # the parameters.  How to do this better?

logging.basicConfig(filename='birdfeeder.log',
                    level=logging.INFO
                    format='%(acstime)s %(message)s')
logging.info("Intializing detectors...")
pir = PIR(PIR_PIN, DETECTOR_DELAY)
ranger = Ranger(TRIG_PIN, ECHO_PIN, SETTLETIME, BACKGROUND, SAMPLES,
                THRESHOLD)
logging.info("Waiting for something to stir...")

while True:
    if pir.listen() and ranger.detect():
        image_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        image_name = image_name + '.jpeg'
        with picamera.PiCamera() as camera:
            camera.rotation = 180
            camera.capture(image_name)
            logging.info('Picture taken')
        if TWEET:
            twitter.update_image(image_name)
        time.sleep(PHOTO_DELAY)
        
