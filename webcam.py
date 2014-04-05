# Module that interfaces with the webcam, taking and recording images.
# Probably uses fswebcam

import subprocess
from PIL import Image
import datetime
import os

def take_snapshot():
    """ Take a snapshot and save it to disk. Return filename of one of the
        shapshots.
        
    """
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = filename + '.jpg'
    p = subprocess.Popen(['fswebcam', '-r', '640x480', '-d', '/dev/video0', filename],
                     cwd=os.getcwd())
    p.communicate() # Wait for the subprocess to complete
    rotate_image(filename)
    return filename

def rotate_image(filename):
    """ Rotate the image in the file 90 degrees counter-clockwise & overwrite. """
    im = Image.open(filename)
    rot = im.rotate(90)
    rot.save(filename)
