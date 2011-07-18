# -*- coding: utf-8 -*-

import time
import urllib.request
import os
import dbm
import bz2
import lxml.objectify
from magnatune.config import config_dir, check_config_dir

import logging

logger = logging.getLogger(__name__)

CRC_URL = 'http://he3.magnatune.com/info/changed.txt'
ALBUM_INFO_URL = 'http://he3.magnatune.com/info/album_info_xml.bz2'

db_file = os.path.join(config_dir, 'api.db')
album_info_file = os.path.join(config_dir, 'album_info.xml')


def download():
    """
    Downloads the last version of the api file from the server.
    """
    source = urllib.request.urlopen(ALBUM_INFO_URL)
    with open(album_info_file, 'wb') as f:
        f.write(bz2.decompress(source.read()))


def update_if_needed():
    """
    Checks if an update of the api file if needed, and download it if needed.
    """
    check_config_dir()
    db = dbm.open(db_file, 'c')
    try:
        updated = float(db.get('updated', 0))
        if time.time() - updated < 60 * 60 * 24:  #24 hours
            logger.debug(
                'Database file updated less than 24 hours, not updating.')
            return

        crc = db.get('crc', None)
        logger.info('Updating CRC file')
        new_crc = urllib.request.urlopen(CRC_URL).read()
        db['updated'] = str(time.time())
        if crc == new_crc:
            logger.debug('Database file up-to-date.')
            return

        logger.info('Updating database file.')
        download()
        db['crc'] = new_crc
    finally:
        db.close()


_db = None


def get_database():
    """
    Returns the api database as an lxml.objectify object, updating the
    database if needed.
    """
    global _db
    if not _db:
        update_if_needed()
        _db = lxml.objectify.parse(album_info_file)
    return _db
