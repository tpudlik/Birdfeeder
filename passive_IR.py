#!/usr/bin/python

""" Passive IR detector interface.  Defines a class PIR that can be used to
    detect motion using the passive IR sensor.
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class PIR():
    """ This object can be used to test whether a bird is present or not,
        using the passive IR sensor.
    """
    
    def __init__(self, pir_pin=18, detector_delay=1):
        """ Initialize a PIR sensor at pin pir_pin, which is to be queried
            once every detector_delay seconds.
        """
        self.pin = pir_pin
        self.previous_pir = 0
        # The use of previous_pir prevents a single detection being
        # reported multiple times.
        self.detector_delay = detector_delay
    
    def listen(self):
        " Loop until a detection event is recorded, then return True."
        GPIO.setup(self.pin, GPIO.IN)
        while True:
            self.current_pir = GPIO.input(self.pin)
            if self.previous_pir == 0 and self.current_pir == 1:
                GPIO.cleanup()
                return True
            self.previous_pir = self.current_pir
            time.sleep(self.detector_delay)


if __name__ == '__main__':
    p = PIR()
    while True: p.listen()
