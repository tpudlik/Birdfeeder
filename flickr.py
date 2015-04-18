#!/usr/bin/python

""" Flickr module: Upload photos to Flickr account. """

import logging
import flickr_api

def upload(filename):
    """Upload the named file to Flickr."""
    logger = logging.getLogger('main.flickr')
    flickr_api.set_auth_handler("flickr_access_token.txt")
    try:
        response = flickr_api.upload(photo_file=filename,
                                     safety_level=1,
                                     is_public=1,
                                     content_type=1)
    except Exception:
        logger.exception("Flickr upload exception")
    else:
        logger.info('Flickr upload: ' + str(response))
