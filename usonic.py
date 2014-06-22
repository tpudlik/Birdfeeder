#!/usr/bin/python

import time
import math
import RPi.GPIO as GPIO

class Ranger:
    """ This object can be used to test whether a bird is present or not.
    """
    
    def __init__(self, trig_pin=23, echo_pin=24, settletime=0.3,
                 bg_stdev=5, background_samples=20, threshold=2):
        """ Initialize the sonic ranger.
                trig_pin: Ranger trigger GPIO pin
                echo_pin: Ranger echo GPIO pin
                settletime: How long to wait after powering ranger before
                    taking measurements?
                bg_stdev: Maximum permissible standard deviation of background
                    measurements (meant to guard against occasional outliers)
                background_samples: Number of background samples to take
                    to estimate the distance in the absence of a bird.
                threshold: How many standard deviations above the background
                    must the signal be to result in a detection event?
        """
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.settletime = settletime
        self.bg_stdev = bg_stdev
        self.threshold = threshold
        self.background, self.deviation = self.get_background(background_samples)
    
    def get_background(self, samples):
        """ Return an estimate the "background" (the reading returned by the
            sensor in the absence of a bird).
        """
        stdev = 2*self.bg_stdev
        # Reject the background estimate if it was corrupted by an outlier.
        while stdev > self.bg_stdev:
            avg, stdev = self.distance(samples)
        return (avg, stdev)
    
    def distance(self, samples):
        """ Take the given number of readings and return their average and
            standard deviation.
        """
        data = []
        for i in range(samples):
            data.append(self.reading())
        average = sum(data)/samples
        
        squares = sum(map(lambda x: x*x, data))/samples
        stdev = math.sqrt((squares - average**2))
        return (average, stdev)
    
    def detect(self):
        """ Measure the distance and return True if the result is more than
            two standard deviations above the background.
        """
        signal = self.reading()
        # We register a detection if the measured distance is _less_ than
        # the background distance.
        if signal < self.background - self.threshold*self.deviation:
            return True
        else:
            return False

    def reading(self):
        " Return the distance to the object in front of the sensor in cm. "
        
        # This is based on code downloaded from,
        # http://www.bytecreation.com/blog/2013/10/13/raspberry-pi-ultrasonic-sensor-hc-sr04
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Pin numbering scheme used, see
        # http://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering

        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trig_pin, GPIO.LOW)
    
        # Allow the sensor to settle
        time.sleep(self.settletime)
    
        # Send 10 microsecond pulse to the trigger pin to activate the sensor.
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        
        # Measure the length of the signal sent by the sensor on the ECHO pin.
        # This is equal to the time the sensor had to wait for the echo of
        # its pulse, i.e. twice the time sound needs to travel the distance
        # to the ranged object.
        while GPIO.input(self.echo_pin) == 0:
            signaloff = time.time()
    
        while GPIO.input(self.echo_pin) == 1:
            signalon = time.time()
        
        try:
            timepassed = signalon - signaloff
        except UnboundLocalError:
            # The sensor has malfunctioned: either signaloff or
            # signalon has not been assigned to.
            timepassed = 0
        
        # Convert to distance assuming the speed of sound is 320 m/s.
        distance = timepassed * 17000
    
        GPIO.cleanup()
        return distance
      
