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

# How many seconds between Tweeted pictures?
PHOTO_DELAY = 60


# Sonic ranger setup
# ==================

# How large is the maximum permissible standard deviation of the background
# signal (in cm)? This setting serves to protect against a background
# measurement corrupted by an outlier.
BACKGROUND = 1

# How many background samples to take when calibrating the ranger (estimating
# the distance measured if there is no bird)?
SAMPLES = 20

# How many samples to take when PIR reports a detection?  (You want to take
# more than one sample because the PIR has a slightly longer range, and
# a detection may be false rejected by the ranger's first reading.)
DETECT_SAMPLES = 2

# How many standard deviations above the background must a signal be to
# count as a detection?
THRESHOLD = 2


# Camera setup
# ============

# How many pictures to take in a row when a detection event has taken place?
PHOTO_BURST = 3


# Twitter integration
# ===================

# Should the photos be tweeted (True or False)?
TWEET = False


# Drobox integration
# ==================

# Should the photos be uploaded to Dropbox (True or False)?
DBOX = True
