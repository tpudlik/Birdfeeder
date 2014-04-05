# Module that interfaces with the webcam, taking and recording images.
# Probably uses fswebcam

import subprocess
import datetime

def shot = take_snapshot():
    """ Take a (succession of?) snapshots and save them to disk. Return
        filename of one of the shapshots.
        
    """
    filename = datetime.datetime.now().strftime("%Y-%M-%d-%H-%M-%S")
    filename = filename + '.jpg'
    subprocess.call('fswebcam -r 640x480 -d /dev/video0 ' + filename)
    return filename
