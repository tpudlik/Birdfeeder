#!/usr/bin/python

""" Dropbox module: allows the uploading of bird snapshots to Dropbox. """

import dropbox
import logging
from access_tokens import D_ACCESS_TOKEN

def upload(filename):
    " Upload the named file to Dropbox. "
    logger = logging.getLogger('main.dbox')
    client = dropbox.client.DropboxClient(D_ACCESS_TOKEN)
    with open(filename, 'rb') as f:
        response = client.put_file('/' + filename, f)
    logger.info('Dropbox upload: ' + str(response)) # TMI?
