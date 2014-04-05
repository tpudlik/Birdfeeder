# main module

""" Check signal from motion sensor every second, take a picture if signal
    is detected."""

import time
import RPi.GPIO as io
import webcam
import twitter

DETECTOR_DELAY = 2 # detector query period, in seconds
PHOTO_DELAY = 30 # minimum delay between photographs, in seconds

io.setmode(io.BCM) # no idea what this does, taken from alarmd.py

pir_pin = 18 # pin on which the passive IR sensor sends data

io.setup(pir_pin, io.IN)

previous_pir = 0
print "Motion detector active, waiting for something to stir..."
while True:
    current_pir = io.input(pir_pin)
    if previous_pir == 0 and current_pir == 1:
        print "Motion detected!"
        shot = webcam.take_snapshot() # shot is the image filename
        twitter.update_image(shot)
        time.sleep(PHOTO_DELAY)
    previous_pir = current_pir
    time.sleep(DETECTOR_DELAY) # Wait for one second
