#!/usr/bin/python

""" postprocess.py: Automatic image enhancement, for use before upload."""

from PIL import Image, ImageOps

def twitter_postprocess(filename):
    """Crop and autocontrast the image in filename, overwrite old image.

    The original image is assumed to have a 4:3 aspect ratio.  The output
    image has a 2:1 aspect ratio.

    """
    original = Image.open(filename)

    # Crop the image
    width, height = original.size   # Get dimensions
    left = 0
    top = height/3
    right = width
    bottom = height
    cropped = original.crop((left, top, right, bottom))

    # Improve the image contrast
    equalized = ImageOps.autocontrast(cropped, cutoff=1)

    # Save the new image
    equalized.save(filename)
