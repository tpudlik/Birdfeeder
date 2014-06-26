# Parameters used by main.py


# GPIO setup
# ==========

# Which GPIO pin (in the BCM scheme) is the PIR detector on?
PIR_PIN = 18

# Which GPIO pin is the sonic ranger trigger on?
TRIG_PIN = 23

# Which GPIO pin is the sonic ranger echo on?
ECHO_PIN = 24


# Delays
# ======

# How many seconds between queries of the PIR?
DETECTOR_DELAY = 1

# For how many seconds should the sonic ranger be allowed to settle?
SETTLETIME = 0.5

# How many seconds between pictures?
PHOTO_DELAY = 5


# Sonic ranger setup
# ==================

# How large is the maximum permissible standard deviation of the background
# signal (in cm)? This setting serves to protect against a background
# measurement corrupted by an outlier.
BACKGROUND = 2

# How many background samples to take when calibrating the ranger (estimating
# the distance measured if there is no bird)?
SAMPLES = 20

# How many standard deviations above the background must a signal be to
# count as a detection?
THRESHOLD = 3


# Twitter integration
# ===================

# Should the photos be tweeted (True or False)?
TWEET = False
