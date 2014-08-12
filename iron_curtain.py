#!/usr/bin/python

""" IR tripwire interface.  Defines a class Tripwire which can be used to
    detect  motion.
    
    The tripwire consists of an IR diode (or a few IR diodes connected in
    series) and an IR detector sensitive to 950 nm radiation modulated at
    38 kHz.  The hardware PWM of the Pi is used to drive the IR diode, which
    continuously emits a square wave at the detector's frequency.
    
    You should always use the Python 'with' statement when creating an
    instance of the Tripwire class to ensure that the sensor and PWM pins
    are properly cleaned up if an exception occurs.
"""

import wiringpi2 as wiringpi
import RPi.GPIO as GPIO
import time
import logging

# Constants
# ============================================================================
PWM_PIN = 18 # This is a hardwired constant since only pin 18 is capable of
             # hardware pulse width modulation (PWM)
# ============================================================================


class Tripwire():

    def __init__(self, sensor_pin=22, detector_delay=1, settletime=0.01):
        """ Initialize the tripwire.  See module documentation for the details
            of the parameter settings used here.
        """
        self.sensor_pin = sensor_pin
        self.detector_delay = detector_delay
        self.logger = logging.getLogger('main.tripwire')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)
        
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(PWM_PIN, 2)
        # Choose mark-space mode for better frequency control
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
        wiringpi.pwmSetRange(2)
        wiringpi.pwmSetClock(253)
        
        wiringpi.pwmWrite(PWM_PIN, 1) # set duty cycle to 1 over range=2, or 50%
        
        time.sleep(settletime) # I'm not sure how long is necessary,
                                  # the demodulator datasheet
                                  # suggests at least 0.0004 s
        self.logger.info('IRon curtain initialized.')

    def listen(self):
        " Wait for a detection event, then return true. "
        time.sleep(self.detector_delay)
        GPIO.wait_for_edge(self.sensor_pin, GPIO.RISING)
        self.logger.info('IRon curtain tripped!')
        return True
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        GPIO.cleanup()
        wiringpi.pwmWrite(PWM_PIN, 0)
        wiringpi.pinMode(PWM_PIN, 0)
        self.logger.info('Cleaned up after IRon curtain.')


if __name__ == '__main__':
    with Tripwire() as t:
        while True: print t.listen()
