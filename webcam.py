# Module that interfaces with the webcam, taking and recording images.
# Probably uses fswebcam

import subprocess
import datetime
import os

def take_snapshot():
    """ Take a snapshot and save it to disk. Return filename of one of the
        shapshots.
        
    """
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = filename + '.jpg'
    p = subprocess.Popen(['fswebcam', '-r', '1280x720',
                          '-d', '/dev/video0',
                          '--rotate', '270',
                          filename],
                         cwd=os.getcwd())
    p.communicate() # Wait for the subprocess to complete
    return filename
