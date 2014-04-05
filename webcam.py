# Module that interfaces with the webcam, taking and recording images.
# Probably uses fswebcam

import subprocess
import datetime
import os

def take_snapshot():
    """ Take a (succession of?) snapshots and save them to disk. Return
        filename of one of the shapshots.
        
    """
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = filename + '.jpg'
    subprocess.Popen(['fswebcam', '-r', '640x480', '-d', '/dev/video0', 'filename'],
                     cwd=os.getcwd())
    return filename
