# Parameters used by main.py


# GPIO setup
# ==========

# Which GPIO pin (in the BCM scheme) is the PIR detector on?
PIR_PIN = 18

# Which GPIO pin is the sonic ranger trigger on?
TRIG = 23

# Which GPIO pin is the sonic ranger echo on?
ECHO = 24


# Delays
# ======

# How many seconds between queries of the PIR?
DETECTOR_DELAY = 1

# For how many seconds should the sonic ranger be allowed to settle?
SETTLETIME = 0.3

# How many seconds between pictures?
PHOTO_DELAY = 5


# Twitter integration
# ===================

# Should the photos be tweeted (True or False)?
TWEET = False
