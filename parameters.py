# Parameters used by main.py


# Pin setup
# =========

# IR sensor pin
SENSOR_PIN = 27


# Delays
# ======

# How many seconds between queries of the tripwire?
DETECTOR_DELAY = 1

# For how many seconds should the tripwire be allowed to settle?
SETTLETIME = 0.01

# How many seconds between Tweeted pictures?
PHOTO_DELAY = 60


# Camera setup
# ============

# How many pictures to take in a row when a detection event has taken place?
PHOTO_BURST = 3

# Should the picture be rotated when it's taken?
# The value of this parameter should be one of the legal input values for
# picamera.PiCamera.rotation, or None.
PHOTO_ROTATE = 180


# Twitter integration
# ===================

# Should the photos be tweeted (True or False)?
TWEET = False


# Drobox integration
# ==================

# Should the photos be uploaded to Dropbox (True or False)?
DBOX = True


# Flickr integration
# ==================

# Should the photos be uploaded to Flickr (True or False)?
FLICKR = False
