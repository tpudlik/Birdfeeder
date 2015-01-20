#!/usr/bin/python

""" IR tripwire interface.  Defines a class Tripwire which can be used to
    detect  motion.
    
    The tripwire consists of an IR diode (or a few IR diodes connected in
    series) and an IR detector sensitive to IR radiation modulated at
    38 kHz.  The hardware PWM of the Pi is used to drive the IR diode, which
    continuously emits a square wave at the detector's frequency.
    
    You should always use the Python 'with' statement when creating an
    instance of the Tripwire class to ensure that the sensor and PWM pins
    are properly cleaned up if an exception occurs.  Since the tripwire is
    usually set up to operate indefinitely from the time it is set up,
    an exception is the only way for it to terminate!  Cleaning up after the
    class is critical, since otherwise a 3V3 PWM signal will continue being
    sent on pin 18; this may destroy any other component connected to the
    pin.  An example of proper syntax is in the "if __name__ == '__main__'"
    block at the end of the module.

    The class constructor takes three optional parameters:
        sensor_pin: the number of the sensor GPIO pin, in the BCM numbering
            scheme.  The default pin is 27, but any GPIO pin except 18
            will do.
        detector_delay: how many seconds to wait before engaging the detector
            again after an event was reported. No delay is probably
            necessary in the default case, but I want to carry out some
            more tests before removing this parameter.
        settletime: how many seconds to wait after engaging the emitter diode
            before beginning to query the detector.  The detector usually
            needs some time to recognize the presence of a signal.  In the
            case of the Adafruit IR sensor I have been using (product no 157),
            this time is supposed to be on the order of 0.0004 seconds.
    
    Both RPi.GPIO and wiringpi2 libraries are used to control the GPIO.  This
    is because as of the creation of this module (August 2014) the RPi.GPIO
    library does not give access to hardware PWM, while the wiringpi2 library
    does not offer a functionality analogous to wait_for_edge (detecting a
    voltage change without repeatedly polling a pin).    

    This class uses the logging standard library module to log events.
"""

import wiringpi2 as wiringpi
import RPi.GPIO as GPIO
import time
import logging

# ============================================================================
PWM_PIN = 18 # This is a hardwired constant since only pin 18 is capable of
             # hardware pulse width modulation (PWM)
# ============================================================================


class Tripwire():

    def __init__(self, sensor_pin=27, detector_delay=1, settletime=0.01):
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
