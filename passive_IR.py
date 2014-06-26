#!/usr/bin/python

""" Passive IR detector interface.  Defines a class PIR that can be used to
    detect motion using the passive IR sensor.
"""

import RPi.GPIO as GPIO
import time
import logging

class PIR():
    """ This object can be used to test whether a bird is present or not,
        using the passive IR sensor.
    """
    
    def __init__(self, pir_pin=18, detector_delay=1):
        """ Initialize a PIR sensor at pin pir_pin, which is to be queried
            once every detector_delay seconds.
        """
        self.pin = pir_pin
        self.detector_delay = detector_delay
        self.logger = logging.getLogger('main.pir')
        
        GPIO.setup(self.pin, GPIO.IN)
        self.logger.info('Passive IR detector initialized')
    
    def listen(self):
        " Wait for a detection event, then return True."
        time.sleep(self.detector_delay)
        GPIO.wait_for_edge(self.pin, GPIO.RISING)
        self.logger.info('Passive IR detected bird')
        return True


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        p = PIR()
        while True: print p.listen()
    finally:
        GPIO.cleanup()
