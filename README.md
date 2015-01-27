Paparazzi Birdfeeder
====================

The paparazzi birdfeeder detects the presence of a bird, takes its picture
and posts the picture to Dropbox or a dedicated Twitter feed.

The hardware consists of a Raspberry Pi camera module, a 38 kHz demodulating
IR sensor (similar to those used in remote-control receivers) and an IR diode.
The entire setup can be powered for hours from a power pack, but is designed
for tethered operation.

## TO DO ##

*   Catch `ErrorResponse` (`dropbox.rest.ErrorResponse`), thrown by the
    Dropbox upload routine when the server makes encounters an error.
    (Currently, the program crashes when this happens.)
*   Don't take pictures after dusk or before dawn (but record events in the
    log).
