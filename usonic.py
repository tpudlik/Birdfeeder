#!/usr/bin/python

# This is based on code downloaded from,
# http://www.bytecreation.com/blog/2013/10/13/raspberry-pi-ultrasonic-sensor-hc-sr04

import time
import RPi.GPIO as GPIO

# Numbers of the pins connected to the sensor
TRIG = 23
ECHO = 24

def reading():
    """ Return the distance to the object in front of the sensor in cm. """

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, GPIO.LOW)

    # Allow the sensor to settle
    time.sleep(0.3)

    # Send 10 microsecond pulse to the trigger pin to activate the sensor.
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    # Measure the length of the signal sent by the sensor on the ECHO pin.
    # This is equal to the time the sensor had to wait for the echo of
    # its pulse, i.e. twice the time sound needs to travel the distance
    # to the ranged object.
    while GPIO.input(ECHO) == 0:
        signaloff = time.time()

    while GPIO.input(ECHO) == 1:
        signalon = time.time()

    timepassed = signalon - signaloff
    
    # Convert to distance assuming the speed of sound is 320 m/s.
    distance = timepassed * 17000

    GPIO.cleanup()
    return distance


if __name__ == '__main__':
    print reading()
