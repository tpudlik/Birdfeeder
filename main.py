# main module

""" Wait for signal from motion sensor, take a picture if signal is detected"""

import time
import RPi.GPIO as io
import webcam
import twitter

io.setmode(io.BCM) # no idea what this does, taken from alarmd.py

pir_pin = 18 # pin on which the passive IR sensor sends data

io.setup(pir_pin, io.IN)

previous_pir = 0
while True:
    current_pir = io.input(pir_pin)
    if previous_pir == 0 and current_pir == 1:
        print "Motion detected!"
        shot = webcam.take_snapshot() # This function not yet implemented,
                                      # may take multiple snapshots in short
                                      # succession
        twitter.update_image(shot) # Tweet the image
    previous_pir = current_pir
    time.sleep(1) # Wait for one second
